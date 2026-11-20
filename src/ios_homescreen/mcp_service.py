"""What the MCP server's tools do, without the MCP SDK.

:class:`Service` reads the phone, plans changes and writes them, the way ``pull``,
``check`` and ``push`` do:

* ``find_phone``, ``read_home_screen``, ``list_apps`` and ``list_backups`` only read.
* ``plan_layout``, ``sort_pages`` and ``plan_restore`` validate a change and list it in
  plain words, without writing. Each plan gets an id.
* ``apply_layout`` and ``restore_backup`` write a plan, and only one this service made,
  with ``confirm`` set. They go through :func:`ios_homescreen.api.push` and
  :func:`ios_homescreen.api.restore`, the one write path the CLI and the editor use:
  backup, write, read back, compare, roll back on a mismatch.

:mod:`ios_homescreen.mcp_server` turns these methods into MCP tools.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from . import api
from .device import DeviceError
from .events import Event
from .model import describe, to_document
from .planner import LayoutError, Plan
from .report import app_places, change_lines, change_summary, library_apps
from .snapshots import device_details, device_of
from .state import StateError, fingerprint, same_layout
from .storage import find_backup, layout_counts
from .transport import Backend, PymobiledeviceBackend, Transport, TransportError
from .workflow import APPLIED, ROLLBACK_FAILED, ROLLED_BACK, Timing, WorkflowError

log = logging.getLogger(__name__)

MAX_PLANS = 20
BACKUPS_LISTED = 20

# Codes that mean "not over this transport" rather than "something is wrong with it",
# the same split the desktop app makes when it tries USB first and Wi-Fi next.
USB_ABSENT_CODES = frozenset({"no_usb_device", "usbmuxd_unreachable"})
WIFI_ABSENT_CODES = frozenset({"not_advertising", "timeout", "no_pair_record"})

DEMO_TIMING = Timing(read_timeout=10, verify_attempts=3, verify_interval=0.2)

Opener = Callable[[], Awaitable[Any]]


class Refused(Exception):
    """A tool refuses before touching the phone; ``code`` is stable for agents."""

    def __init__(self, message: str, *, code: str, steps: list[str] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.steps = steps or []


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    backup_dir: Path
    timing: Timing = field(default_factory=Timing)
    transport: Transport = field(default_factory=Transport)
    """The UDID and time limits; with ``auto`` its ``wifi`` is ignored."""
    auto: bool = True
    """USB when a cable is in, otherwise Wi-Fi, like the desktop app."""
    demo: bool = False


@dataclass
class _Pending:
    """A planned write waiting for the person's yes."""

    kind: str
    """``layout`` or ``restore``."""
    target: dict[str, Any]
    before: str
    """Fingerprint of the phone's layout the change list was made against."""


def _plan_id(kind: str, target: Any, before: str) -> str:
    text = f"{kind}:{before}:{fingerprint(target)}"
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _changes(changes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "changes": change_lines(changes),
        "summary": change_summary(changes),
        "change_list": changes,
    }


def _is_document(layout: Mapping[str, Any]) -> bool:
    """The layout file's structure (``dock = {items = [...]}``) rather than the read's."""
    return isinstance(layout.get("dock"), Mapping)


def _check_shape(layout: Mapping[str, Any]) -> None:
    """A wrong shape would silently plan every app into the App Library; refuse it."""
    if "pages" not in layout or not isinstance(layout["pages"], list):
        raise Refused(
            "the layout needs a 'pages' list (each page {\"items\": [...]}, or a plain list of "
            "items), and a 'dock' list; the same structure read_home_screen returns",
            code="bad_layout",
        )
    if not _is_document(layout) and not isinstance(layout.get("dock", []), list):
        raise Refused("'dock' must be a list of items", code="bad_layout")


class Service:
    """What the tools do, without the MCP SDK. One phone operation runs at a time."""

    def __init__(
        self,
        settings: Settings,
        *,
        opener: Opener | None = None,
        backend: Backend | None = None,
    ) -> None:
        self.settings = settings
        self._opener = opener
        self._backend = backend
        self._busy = asyncio.Lock()
        self.read: dict[str, Any] | None = None
        self.pull: Path | None = None
        self.pending: dict[str, _Pending] = {}

    @classmethod
    def demo(cls, data_dir: Path, *, delay: float = 0.1) -> Service:
        """A server on the editor's pretend iPhone: no phone needed, writes go to it."""
        from .ui.demo import DemoDevice

        device = DemoDevice(delay=delay)

        async def opener() -> Any:
            return device

        settings = Settings(
            data_dir=data_dir, backup_dir=data_dir / "backups", timing=DEMO_TIMING, demo=True
        )
        return cls(settings, opener=opener)

    # ------------------------------------------------------------------ connection

    async def _open(self) -> Any:
        if self._opener is not None:
            return await self._opener()
        transport = self.settings.transport
        if not self.settings.auto:
            return await api.connect(transport, backend=self._backend)
        try:
            return await api.connect(replace(transport, wifi=False), backend=self._backend)
        except TransportError as exc:
            if exc.code not in USB_ABSENT_CODES:
                raise
        try:
            return await api.connect(replace(transport, wifi=True), backend=self._backend)
        except TransportError as exc:
            if exc.code not in WIFI_ABSENT_CODES:
                raise
            raise TransportError(
                "no iPhone found over USB or on the network", code="no_device"
            ) from exc

    @contextlib.asynccontextmanager
    async def _phone(self) -> AsyncIterator[Any]:
        """Connect for one operation and close afterwards, like the CLI."""
        async with self._busy:
            device = await self._open()
            try:
                yield device
            finally:
                if not self.settings.demo:
                    await device.close()

    def _connection(self, device: Any) -> str:
        return "demo" if self.settings.demo else str(getattr(device, "transport", "usb"))

    # ------------------------------------------------------------------ reading

    async def find_phone(self) -> dict[str, Any]:
        try:
            async with self._phone() as device:
                info = device_details(device.info)
                connection = self._connection(device)
                wifi: dict[str, Any] = {}
                with contextlib.suppress(Exception):
                    wifi["enabled"] = await device.wifi_connections_enabled()
        except (TransportError, DeviceError, OSError, TimeoutError) as exc:
            problem = friendly_error(exc)
            return {
                "found": False,
                "problem": problem,
                "next_step": " ".join(problem["steps"]) or "Connect the iPhone and try again.",
            }
        if not self.settings.demo:
            with contextlib.suppress(Exception):
                backend = self._backend or PymobiledeviceBackend()
                udid = info.get("udid", "").lower()
                wifi["paired_with_this_computer"] = any(
                    r.udid.strip().lower() == udid and r.usable for r in backend.remote_records()
                )
        return {
            "found": True,
            "device": info,
            "connection": connection,
            "trusted": True,
            "wifi": wifi,
            "demo": self.settings.demo,
            "next_step": "Call read_home_screen to see the layout.",
        }

    async def _read_phone(self) -> dict[str, Any]:
        async with self._phone() as device:
            snapshot = await api.read_device(device)
        self._keep(snapshot)
        return snapshot

    def _keep(self, snapshot: dict[str, Any]) -> None:
        self.pull = api.save_pull(snapshot, self.settings.data_dir)
        self.read = snapshot

    async def _base(self) -> dict[str, Any]:
        """The read plans are made against: the last one, or a fresh one."""
        return self.read if self.read is not None else await self._read_phone()

    async def read_home_screen(self, include_toml: bool = False) -> dict[str, Any]:
        snapshot = await self._read_phone()
        assert self.pull is not None
        view = describe(snapshot)
        counts = layout_counts(snapshot["state"])
        result: dict[str, Any] = {
            "device": view["device"],
            "pull": self.pull.name,
            "pull_path": str(self.pull),
            "summary": {
                "dock_items": counts["dock"],
                "pages": counts["pages"],
                "app_library_only": len(view["library"]),
            },
            "limits": view["limits"],
            "dock": view["dock"],
            "pages": [{"page": n, **page} for n, page in enumerate(view["pages"], 1)],
            "library": view["library"],
        }
        if include_toml:
            result["toml"] = api.export_layout(
                snapshot, pull=self.pull.name, note=api.pull_note(snapshot)
            )
        return result

    async def list_apps(self, query: str | None = None) -> dict[str, Any]:
        read = await self._base()
        found = app_places(read)
        wanted = (query or "").casefold()
        if wanted:
            found = [a for a in found if wanted in a["name"].casefold() or wanted in a["id"]]
        return {"pull": self.pull.name if self.pull else None, "apps": found}

    def list_backups(self, limit: int = BACKUPS_LISTED) -> dict[str, Any]:
        found = api.list_backups(self.settings.backup_dir, limit=max(1, limit))
        return {
            "directory": str(self.settings.backup_dir),
            "backups": [backup.to_dict() for backup in found],
            "next_step": "To undo a write, call plan_restore with a backup name ('latest' for "
            "the newest)."
            if found
            else "No backups yet: every write makes one first.",
        }

    # ------------------------------------------------------------------ planning

    def _remember(self, kind: str, pending: _Pending) -> str:
        ident = _plan_id(kind, pending.target, pending.before)
        self.pending.pop(ident, None)
        self.pending[ident] = pending
        while len(self.pending) > MAX_PLANS:
            self.pending.pop(next(iter(self.pending)))
        return ident

    def _document(self, layout: Mapping[str, Any] | None, toml: str | None) -> Any:
        if (layout is None) == (toml is None):
            raise Refused("pass either layout or toml, not both and not neither", code="bad_layout")
        if toml is not None:
            return api.load_layout(toml)
        assert layout is not None
        _check_shape(layout)
        return layout if _is_document(layout) else to_document(layout)

    def _planned(self, plan: Plan, read: dict[str, Any]) -> dict[str, Any]:
        apps = read.get("apps", {}) or {}
        result: dict[str, Any] = {
            "valid": True,
            "unchanged": plan.unchanged,
            "plan_id": None,
            **_changes(list(plan.change_list)),
            "app_library_only": len(library_apps(plan.payload, apps)),
            "based_on": {"pull": self.pull.name if self.pull else None, **read.get("device", {})},
        }
        if plan.unchanged:
            result["next_step"] = "Nothing would change; there is nothing to apply."
            return result
        before = fingerprint(read["state"])
        result["plan_id"] = self._remember("layout", _Pending("layout", plan.payload, before))
        result["next_step"] = (
            "Show the person these changes in plain words and ask whether to write them to "
            "their iPhone. Only after an explicit yes, call apply_layout with this plan_id and "
            "confirm=true."
        )
        return result

    def _invalid(self, error: LayoutError) -> dict[str, Any]:
        return {
            "valid": False,
            "plan_id": None,
            "issues": error.to_dict()["issues"],
            "next_step": "Fix every issue (each has a code, a location and a message) and call "
            "plan_layout again.",
        }

    async def plan_layout(
        self,
        layout: Mapping[str, Any] | None = None,
        toml: str | None = None,
        allow_removal: bool = False,
    ) -> dict[str, Any]:
        document = self._document(layout, toml)
        read = await self._base()
        try:
            plan = api.plan_layout(document, read, allow_removal=allow_removal)
        except LayoutError as error:
            return self._invalid(error)
        return self._planned(plan, read)

    async def sort_pages(
        self,
        layout: Mapping[str, Any] | None = None,
        toml: str | None = None,
        allow_removal: bool = False,
    ) -> dict[str, Any]:
        read = await self._base()
        apps = read.get("apps", {}) or {}
        try:
            if layout is None and toml is None:
                state: Any = read["state"]
            else:
                document = self._document(layout, toml)
                state = api.plan_layout(document, read, allow_removal=allow_removal).payload
            # The same steps as `ios-homescreen sort`: sort, write as a layout, plan that.
            text = api.export_layout({"state": api.sort_state(state), "apps": apps})
            plan = api.plan_layout(text, read, allow_removal=allow_removal)
        except LayoutError as error:
            return self._invalid(error)
        result = self._planned(plan, read)
        view = describe({"state": plan.payload, "apps": apps})
        result["layout"] = {
            "dock": view["dock"],
            "pages": [{"page": n, **page} for n, page in enumerate(view["pages"], 1)],
        }
        return result

    async def plan_restore(
        self, backup: str = "latest", allow_other_device: bool = False
    ) -> dict[str, Any]:
        # Only backup names: an agent cannot point a write at any file on the computer.
        path = find_backup(self.settings.backup_dir, backup, allow_paths=False)
        target = api.load_backup(path)
        recorded = device_of(path)
        async with self._phone() as device:
            info = dict(device.info)
            wanted, actual = recorded.get("udid"), info.get("udid")
            if wanted and actual and wanted != actual and not allow_other_device:
                raise Refused(
                    f"{path.name} was made on another iPhone ({recorded.get('name') or wanted}); "
                    "nothing was planned. Restore it to this phone only if the person asks for "
                    "that, with allow_other_device=true.",
                    code="other_device",
                )
            current = await device.read_state()
            apps = await device.installed_apps()
        result: dict[str, Any] = {"backup": path.name, "made_on": recorded}
        if same_layout(current, target):
            return {
                **result,
                "unchanged": True,
                "plan_id": None,
                **_changes([]),
                "next_step": "The iPhone already shows this backup; there is nothing to restore.",
            }
        changes = api.changes_between({"state": current, "apps": apps}, target)
        pending = _Pending("restore", target, fingerprint(current))
        return {
            **result,
            "unchanged": False,
            "plan_id": self._remember("restore", pending),
            **_changes(changes),
            "next_step": "Show the person these changes in plain words and ask whether to "
            "restore this backup. Only after an explicit yes, call restore_backup with this "
            "plan_id and confirm=true.",
        }

    # ------------------------------------------------------------------ writing

    def _take(self, plan_id: str, kind: str, confirm: bool) -> _Pending:
        tool = {"layout": "plan_layout or sort_pages", "restore": "plan_restore"}[kind]
        pending = self.pending.get(plan_id)
        if pending is None or pending.kind != kind:
            raise Refused(
                f"there is no {kind} plan with id {plan_id!r} in this session; nothing was "
                f"written. Call {tool} first and use the plan_id it returns.",
                code="unknown_plan",
            )
        if confirm is not True:
            raise Refused(
                "confirm must be true, and only after the person said yes to this plan's change "
                "list; nothing was written.",
                code="confirmation_needed",
            )
        return pending

    def _result(self, result: api.ApplyResult, events: list[Event]) -> dict[str, Any]:
        out: dict[str, Any] = {
            "status": result.status,
            "written": True,
            "verified": result.status == APPLIED,
            "rolled_back": result.status == ROLLED_BACK,
            "backup": result.backup.name,
            "backup_path": str(result.backup),
            "write_unconfirmed": result.write_unconfirmed,
            "messages": [event.message for event in events],
        }
        if result.status == APPLIED:
            out["next_step"] = (
                "Tell the person it is done. list_backups and plan_restore can undo it."
            )
        elif result.status == ROLLED_BACK:
            out["next_step"] = (
                "The phone did not show the new layout in time, so the backup was written back "
                "and verified: the phone is as it was. Tell the person; trying again later "
                "usually works."
            )
        elif result.status == ROLLBACK_FAILED:
            out["next_step"] = (
                "Tell the person now: the rollback could not be verified either. They should "
                f"look at the phone; the backup {result.backup.name} is kept and plan_restore "
                "can write it back after their yes."
            )
        return out

    async def _write(
        self, plan_id: str, pending: _Pending, write: Callable[..., Awaitable[api.ApplyResult]]
    ) -> dict[str, Any]:
        events: list[Event] = []
        async with self._phone() as device:
            self.pending.pop(plan_id, None)  # one write per plan, whatever happens next
            result = await write(device, events.append)
            out = self._result(result, events)
            try:
                snapshot = await api.read_device(device)
            except Exception as exc:
                out["new_pull"] = None
                log.warning("reading the phone after the write failed: %s", exc)
            else:
                self._keep(snapshot)
                out["new_pull"] = self.pull.name if self.pull else None
        return out

    async def apply_layout(self, plan_id: str, confirm: bool = False) -> dict[str, Any]:
        pending = self._take(plan_id, "layout", confirm)
        settings = self.settings

        async def write(device: Any, emit: Callable[[Event], None]) -> api.ApplyResult:
            # api.push refuses (layout_changed) when the phone changed since the read the
            # plan was made against: then the change list the person saw is not the truth.
            return await api.push(
                device,
                pending.target,
                backup_dir=settings.backup_dir,
                timing=settings.timing,
                on_event=emit,
            )

        return await self._write(plan_id, pending, write)

    async def restore_backup(self, plan_id: str, confirm: bool = False) -> dict[str, Any]:
        pending = self._take(plan_id, "restore", confirm)
        settings = self.settings

        async def write(device: Any, emit: Callable[[Event], None]) -> api.ApplyResult:
            # A restore overwrites on purpose (api.restore has no drift check), so check here
            # that the phone still shows what the change list was made against.
            current = await device.read_state()
            if fingerprint(current) != pending.before:
                raise WorkflowError(
                    "the phone's layout changed since plan_restore, so its change list is out "
                    "of date; nothing was written. Call plan_restore again and show the new list.",
                    code="layout_changed",
                )
            return await api.restore(
                device,
                pending.target,
                backup_dir=settings.backup_dir,
                timing=settings.timing,
                on_event=emit,
            )

        return await self._write(plan_id, pending, write)


# --------------------------------------------------------------------------- errors


_EXTRA_STEPS = {
    "busy": [
        "Another IconShuffle window, command or agent is writing to the phone.",
        "Wait until it has finished, then read the home screen again and plan again.",
    ],
    "layout_changed": [
        "The home screen changed since it was read (on the phone, in the editor, or by "
        "another write). Nothing was written.",
        "Call read_home_screen, rebuild the layout, plan it and ask the person again.",
    ],
}


def friendly_error(exc: BaseException) -> dict[str, Any]:
    """``{code, title, message, steps}`` for an error, with steps written for this server."""
    if isinstance(exc, Refused):
        return {"code": exc.code, "title": "Refused", "message": str(exc), "steps": exc.steps}
    from .ui.errors import friendly

    found = friendly(exc)
    steps = _EXTRA_STEPS.get(found["code"]) or found["steps"]
    return {
        "code": found["code"],
        "title": found["title"],
        "message": str(exc),
        # The editor's wording; here the MCP client starts the server.
        "steps": [
            step.replace("Restart the editor with", "Start the server with") for step in steps
        ],
    }


EXPECTED_ERRORS = (
    Refused,
    LayoutError,
    StateError,
    WorkflowError,
    DeviceError,
    TransportError,
    OSError,
    TimeoutError,
)
