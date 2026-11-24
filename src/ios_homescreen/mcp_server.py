"""The MCP server: ``ios-homescreen mcp`` lets AI assistants rearrange the home screen.

It speaks the Model Context Protocol over stdio, so Claude Desktop, Claude Code, Codex,
Cursor, VS Code and other MCP clients start it as a subprocess. stdout carries only the
protocol; logs go to stderr. The tools are thin wrappers around
:class:`ios_homescreen.mcp_service.Service`: reads, plans that write nothing, and two
writes (``apply_layout``, ``restore_backup``) that need a plan id and ``confirm``.

This module needs the MCP SDK (the optional ``mcp`` extra); the CLI imports it only for
``ios-homescreen mcp``.
"""

from __future__ import annotations

import json
import logging
import tempfile
from collections.abc import Awaitable
from pathlib import Path
from typing import Annotated, Any

import anyio
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from . import __version__
from .mcp_service import BACKUPS_LISTED, EXPECTED_ERRORS, Service, Settings, friendly_error
from .planner import LayoutError

NAME = "iconshuffle"

INSTRUCTIONS = """\
IconShuffle reads and rearranges the home screen of the person's iPhone (connected to \
this computer over USB or Wi-Fi). The safe flow, always:

1. find_phone if you are not sure a phone is connected; follow its next_step if not.
2. read_home_screen (and list_apps) to see the dock, pages, folders, widgets and the \
App Library.
3. Build the layout the person asked for and call plan_layout (or sort_pages for A-Z). \
Fix every issue it reports and plan again until it is valid.
4. Show the person the change list in plain words and ask whether to write it to their \
iPhone. Wait for an explicit yes in this conversation.
5. Only then call apply_layout with the plan_id and confirm=true, and report the result.

Never call apply_layout or restore_backup without that yes. Never leave widgets, web \
clips or web apps out of a layout unless the person asked to remove widgets (web clips \
and web apps cannot be removed at all). To undo, use list_backups, plan_restore and, \
after a yes, restore_backup. Every write is backed up, read back, and rolled back on its \
own if the phone does not show the new layout."""


LAYOUT_HELP = (
    "The layout to plan, in the structure read_home_screen returns: "
    '{"dock": [items], "pages": [{"items": [items]}, ...]}. An item is an app\'s bundle id or '
    'its exact name as a string, an item object from read_home_screen (only "type" and "id" '
    'matter), or a folder {"type": "folder", "name": "Work", "items": [...]} (or "pages": '
    "[[...], [...]] for a folder with several pages). Widgets, web clips and web apps are "
    '{"type": "widget"|"webclip"|"webapp", "id": "..."} from the read. Apps in no dock or page '
    "go to the App Library and stay installed. Pass this or toml, not both."
)
TOML_HELP = (
    "The same layout as TOML text in the format of `ios-homescreen pull` (read_home_screen "
    "with include_toml=true returns it). A [pull] table in it is ignored: the plan is always "
    "made against the last read. Pass this or layout, not both."
)
REMOVAL_HELP = (
    "Let the layout remove widgets it leaves out. Only when the person asked to remove those "
    "widgets; web clips and web apps can never be removed."
)

# Module level: the SDK reads the tools' annotations from the module's globals.
Layout = Annotated[dict[str, Any] | None, Field(description=LAYOUT_HELP)]
Toml = Annotated[str | None, Field(description=TOML_HELP)]
Removal = Annotated[bool, Field(description=REMOVAL_HELP)]


def build_server(service: Service) -> Any:
    """The MCP server for ``service``, with its tools and a prompt."""
    server = MCPServer(
        NAME,
        title="IconShuffle",
        instructions=INSTRUCTIONS,
        website_url="https://iconshuffle.app",
        version=__version__,
        log_level="WARNING",
    )

    def reads(title: str) -> ToolAnnotations:
        return ToolAnnotations(title=title, readOnlyHint=True, openWorldHint=False)

    def writes(title: str) -> ToolAnnotations:
        return ToolAnnotations(
            title=title,
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
            openWorldHint=False,
        )

    async def call(work: Awaitable[dict[str, Any]]) -> dict[str, Any]:
        try:
            return await work
        except EXPECTED_ERRORS as exc:
            if isinstance(exc, LayoutError):
                error = {"code": "layout_invalid", "message": str(exc), **exc.to_dict()}
            else:
                error = friendly_error(exc)
            raise ToolError(json.dumps({"error": error}, ensure_ascii=False)) from exc

    @server.tool(annotations=reads("Find the iPhone"))
    async def find_phone() -> dict[str, Any]:
        """Check whether an iPhone is connected (USB first, then Wi-Fi) and trusts this
        computer. Returns found, the device (name, model, iOS version), the connection, and
        the Wi-Fi setup. When none is found it returns problem and next_step: tell the person
        what to do (plug in, unlock, tap Trust This Computer), then call it again."""
        return await call(service.find_phone())

    @server.tool(annotations=reads("Read the home screen"))
    async def read_home_screen(
        include_toml: Annotated[
            bool, Field(description="Also return the layout as editable TOML text.")
        ] = False,
    ) -> dict[str, Any]:
        """Read the iPhone's home screen (nothing is written to the phone). Returns the dock,
        every page with its items in order (apps, folders with their pages, widgets with
        size and cells, web clips, web apps), the apps only in the App Library, the limits
        (dock items, cells per page), and the saved snapshot. Plans are made against this
        read; read again after the phone was changed elsewhere."""
        return await call(service.read_home_screen(include_toml))

    @server.tool(annotations=reads("List the apps"))
    async def list_apps(
        query: Annotated[
            str | None, Field(description="Only apps whose name or bundle id contains this.")
        ] = None,
    ) -> dict[str, Any]:
        """List the installed apps a person can see, with name, bundle id, type and where each
        one is: the dock, a page and position, a folder, or only the App Library. Uses the
        last read (reads the phone if there is none). Use the names or ids in a layout."""
        return await call(service.list_apps(query))

    @server.tool(annotations=reads("Plan a layout"))
    async def plan_layout(
        layout: Layout = None,
        toml: Toml = None,
        allow_removal: Removal = False,
    ) -> dict[str, Any]:
        """Validate a new home screen layout against the last read and list what writing it
        would change, in plain words. Writes nothing. The dock holds at most 4 items, a page
        24 cells (apps, folders, web clips and web apps 1; widgets 4, 8 or 16); folders hold
        apps, web clips and web apps; keep every widget, web clip and web app. A valid plan
        returns a plan_id and the change list; an invalid one returns issues to fix. Then show
        the person the changes and ask; apply_layout writes the plan after their yes."""
        return await call(service.plan_layout(layout, toml, allow_removal))

    @server.tool(annotations=reads("Sort pages A-Z"))
    async def sort_pages(
        layout: Annotated[
            dict[str, Any] | None,
            Field(
                description="A layout to sort instead of the phone's current one. " + LAYOUT_HELP
            ),
        ] = None,
        toml: Toml = None,
        allow_removal: Removal = False,
    ) -> dict[str, Any]:
        """Plan every page's apps, folders, web clips and web apps in A-Z name order, the same
        rules as `ios-homescreen sort` and the editor's Sort A-Z: the dock, folder contents
        and widgets keep their places, each page keeps its size. Writes nothing. Returns the
        sorted layout, the change list and a plan_id for apply_layout (after the person's
        yes)."""
        return await call(service.sort_pages(layout, toml, allow_removal))

    @server.tool(annotations=writes("Write a planned layout"))
    async def apply_layout(
        plan_id: Annotated[str, Field(description="The plan_id from plan_layout or sort_pages.")],
        confirm: Annotated[
            bool,
            Field(description="Must be true: the person said yes to this plan's change list."),
        ] = False,
    ) -> dict[str, Any]:
        """Write a planned layout to the iPhone. Before calling it, show the person the plan's
        change list and get an explicit yes in this conversation; never call it on your own.
        It saves a backup, writes, reads the phone back and compares; if the phone does not
        show the new layout, the backup is written back on its own. It refuses an unknown
        plan_id, confirm other than true, and a phone that changed since the plan's read.
        Returns status (applied, rolled-back or rollback-failed) and the backup."""
        return await call(service.apply_layout(plan_id, confirm))

    @server.tool(annotations=reads("List the backups"))
    async def list_backups(
        limit: Annotated[int, Field(description="How many, newest first.", ge=1)] = (
            BACKUPS_LISTED
        ),
    ) -> dict[str, Any]:
        """List the backups saved before every write (by this server, the app or the command
        line), newest first: name, when, which iPhone, and what the layout held."""
        return service.list_backups(limit)

    @server.tool(annotations=reads("Plan a restore"))
    async def plan_restore(
        backup: Annotated[
            str, Field(description="A backup name from list_backups, or 'latest'.")
        ] = "latest",
        allow_other_device: Annotated[
            bool,
            Field(
                description="Restore a backup made on another iPhone; only if the person "
                "asked for that."
            ),
        ] = False,
    ) -> dict[str, Any]:
        """Plan writing a backup back (to undo a write): reads the phone and lists what the
        restore would change, in plain words. Writes nothing. Returns a plan_id for
        restore_backup, which writes it after the person's yes."""
        return await call(service.plan_restore(backup, allow_other_device))

    @server.tool(annotations=writes("Restore a backup"))
    async def restore_backup(
        plan_id: Annotated[str, Field(description="The plan_id from plan_restore.")],
        confirm: Annotated[
            bool,
            Field(description="Must be true: the person said yes to this restore's changes."),
        ] = False,
    ) -> dict[str, Any]:
        """Write a planned restore to the iPhone, with the same steps as apply_layout: a backup
        of the current layout first, then write, read back, compare, roll back on a mismatch.
        Only after the person said yes to plan_restore's change list in this conversation."""
        return await call(service.restore_backup(plan_id, confirm))

    @server.prompt(title="Organize my home screen")
    def organize_home_screen(
        request: Annotated[
            str, Field(description="What the person wants, for example 'games on page 2'.")
        ] = "",
    ) -> str:
        """Rearrange the iPhone home screen safely: read, plan, ask, then write."""
        wish = request.strip() or "Ask me what I would like to change."
        return (
            "Help me rearrange my iPhone home screen with the IconShuffle tools.\n\n"
            f"{INSTRUCTIONS}\n\n"
            "Decide categories such as games or work apps from the app names yourself and ask "
            "me when you are unsure. Keep the dock to 4 items and every page within 24 cells.\n\n"
            f"What I want: {wish}"
        )

    return server


def serve(service: Service) -> int:
    """Run the stdio server until the client closes it."""
    server = build_server(service)
    # The SDK points fd 1 at stderr while it serves, so nothing but the protocol reaches
    # stdout, not even a stray print in a dependency.
    anyio.run(server.run_stdio_async)
    return 0


def main(settings: Settings, *, demo: bool = False) -> int:
    """``ios-homescreen mcp``: serve the phone ``settings`` describe, or with ``demo`` the
    pretend one (then ``settings`` is not used)."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    if demo:
        # Demo mode never touches the real data directory.
        with tempfile.TemporaryDirectory(prefix="ihs-mcp-demo-") as scratch:
            return serve(Service.demo(Path(scratch)))
    return serve(Service(settings))


__all__ = ["build_server", "main", "serve"]
