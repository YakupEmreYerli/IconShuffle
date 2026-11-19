"""What differs between Linux, macOS and Windows, run on each of them in CI.

The whole workflow runs against a fake phone with names in several scripts, on files a
Windows editor would leave behind. The USB connection runs through pymobiledevice3 to a
pretend usbmuxd on real sockets at the OS's own address, and the Wi-Fi lookup through the
OS's real network stack. Only the cable and a real iPhone are missing.
"""

from __future__ import annotations

import asyncio
import io
import json
import os
import plistlib
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

import samples
from fake_usbmuxd import WINDOWS_ADDRESS, FakeUsbmuxd
from fakes import FakeSpringBoard, opener_for
from ios_homescreen.cli import main
from ios_homescreen.state import load_plist, same_layout
from ios_homescreen.transport import (
    AddressMemory,
    PymobiledeviceBackend,
    RemoteRecord,
    Transport,
    TransportError,
    connect,
    usb_service_help,
)
from ios_homescreen.ui.errors import classify, friendly

FAST = ["--verify-attempts", "2", "--verify-interval", "0", "--write-timeout", "1"]
FOLDER = "Oyunlar ışığı ✨"
RENAMED = "Müzik 🎵 日本"
IN_CI = bool(os.environ.get("CI"))


@pytest.fixture
def home(tmp_path, monkeypatch) -> Path:
    monkeypatch.setenv("IOS_HOMESCREEN_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    return tmp_path / "data"


def localized_phone(**kwargs) -> FakeSpringBoard:
    """The sample home screen with its Utilities folder named in Turkish, with an emoji."""
    state = samples.home_screen()
    folder = next(i for i in state[1] if isinstance(i, dict) and i.get("listType") == "folder")
    folder["displayName"] = FOLDER
    return FakeSpringBoard(state, samples.installed_apps(), **kwargs)


def folder_names(device: FakeSpringBoard) -> list[str]:
    state = asyncio.run(device.read_state())
    return [
        i["displayName"]
        for page in state[1:]
        for i in page
        if isinstance(i, dict) and "listType" in i
    ]


def save_like_notepad(path: Path, text: str) -> None:
    """Windows line endings and a byte order mark, as some Windows editors save."""
    path.write_text(text, encoding="utf-8-sig", newline="\r\n")


def run_json(argv, capsys, **kwargs) -> tuple[int, dict]:
    capsys.readouterr()
    code = main([*argv, "--json"], **kwargs)
    return code, json.loads(capsys.readouterr().out)


# ------------------------------------------------------------------ the whole workflow


def test_pull_edit_check_push_rollback_restore_on_this_os(home, capsys):
    device = localized_phone()
    layout = Path("layout.toml")

    # pull: the layout file holds the names exactly, whatever the OS writes as newline.
    assert main(["pull"], open_device=opener_for(device)) == 0
    text = layout.read_text(encoding="utf-8")
    assert f'name = "{FOLDER}"' in text

    # edit in a Windows editor: rename the folder, save with CRLF and a BOM.
    save_like_notepad(layout, text.replace(FOLDER, RENAMED))

    code, result = run_json(["check"], capsys)
    assert code == 0, result
    assert result["valid"] is True
    assert "folder_renamed" in {c["kind"] for c in result["changes"]}

    # push: backup, write, verify; the file is pointed at the new pull, BOM and CRLF kept.
    code, result = run_json(["push", "--yes", *FAST], capsys, open_device=opener_for(device))
    assert code == 0, result
    assert RENAMED in folder_names(device)
    (backup,) = (home / "backups").glob("backup-*.plist")
    assert same_layout(load_plist(backup)["state"], asyncio.run(localized_phone().read_state()))
    raw = layout.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" in raw
    assert b"\n" not in raw.replace(b"\r\n", b"")
    code, result = run_json(["check"], capsys)
    assert code == 0
    assert result["unchanged"] is True

    # a write the phone ignores is rolled back: exit code 3, the phone as it was.
    device.ignore_writes = True
    save_like_notepad(layout, layout.read_text(encoding="utf-8-sig").replace(RENAMED, "Other"))
    assert main(["push", "--yes", *FAST], open_device=opener_for(device)) == 3
    assert RENAMED in folder_names(device)
    device.ignore_writes = False

    # restore the backup made before the first push: the original name is back.
    code, result = run_json(["backups"], capsys)
    assert code == 0
    first = min(result["backups"], key=lambda b: b["name"])["name"]
    code, result = run_json(
        ["restore", first, "--yes", *FAST], capsys, open_device=opener_for(device)
    )
    assert code == 0, result
    assert FOLDER in folder_names(device)


def test_a_pipe_that_cannot_show_every_name_still_gets_the_answer(home):
    """A Windows pipe uses the ANSI code page (cp1252 and the like), not UTF-8: the CLI
    must not crash on a folder name it cannot encode, and --json must stay exact."""
    assert main(["pull"], open_device=opener_for(localized_phone())) == 0
    layout = Path("layout.toml")
    layout.write_text(layout.read_text(encoding="utf-8").replace(FOLDER, RENAMED), encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}

    def run(*argv):
        return subprocess.run(
            [sys.executable, "-m", "ios_homescreen", *argv],
            env=env,
            capture_output=True,
            timeout=60,
        )

    text = run("check")
    as_json = run("check", "--json")

    assert text.returncode == 0, text.stderr.decode("cp1252", "replace")
    assert as_json.returncode == 0, as_json.stderr.decode("cp1252", "replace")
    result = json.loads(as_json.stdout.decode("cp1252"))
    assert RENAMED in json.dumps(result["changes"], ensure_ascii=False)


# ------------------------------------------------------------------ messages that name OS services


@pytest.mark.parametrize(
    ("platform", "named", "not_named"),
    [
        ("linux", "systemctl start usbmuxd", "Apple Mobile Device Service"),
        ("darwin", "part of macOS", "systemctl"),
        ("win32", "Apple Mobile Device Service", "systemctl"),
    ],
)
def test_usb_service_help_names_this_os_service(platform, named, not_named):
    unreachable, restart = usb_service_help(platform)

    assert named in unreachable
    assert not_named not in unreachable + restart


def test_the_editor_names_this_os_usb_service():
    """``ui.errors`` picks its text when imported, so this checks the OS it runs on."""
    title = friendly(TransportError("x", code="usbmuxd_unreachable"))["title"]
    expected = {
        "darwin": "The iPhone connection service did not answer",
        "win32": "Apple Devices is not installed",
    }.get(sys.platform, "usbmuxd is not running")

    assert title == expected


# ------------------------------------------------------------------ USB through a pretend usbmuxd


@pytest.fixture
def pymobiledevice3_home(tmp_path, monkeypatch) -> Path:
    """pymobiledevice3 keeps pair records in its own folder; keep it in the test."""
    common = pytest.importorskip("pymobiledevice3.common")
    folder = tmp_path / "pymobiledevice3"
    folder.mkdir()
    monkeypatch.setattr(common, "_HOMEFOLDER", folder)
    return folder


@pytest.fixture
def usbmuxd(monkeypatch, pymobiledevice3_home):
    """Start a :class:`FakeUsbmuxd` where pymobiledevice3 looks on this OS; yields a
    function that runs a coroutine with the service up."""

    def serve(fake: FakeUsbmuxd, work):
        async def main():
            if sys.platform == "win32":
                # The real address: what Apple Mobile Device Service listens on.
                monkeypatch.delenv("USBMUXD_SOCKET_ADDRESS", raising=False)
                try:
                    server = await asyncio.start_server(fake.handle, *WINDOWS_ADDRESS)
                except OSError:
                    pytest.skip("port 27015 is taken (Apple Mobile Device Service runs here)")
            else:
                # A Unix socket like /var/run/usbmuxd; short path for macOS's 104 bytes.
                folder = tempfile.mkdtemp(prefix="mux", dir="/tmp")
                path = os.path.join(folder, "usbmuxd")
                monkeypatch.setenv("USBMUXD_SOCKET_ADDRESS", path)
                server = await asyncio.start_unix_server(fake.handle, path)
            async with server:
                return await work()

        return asyncio.run(main())

    return serve


def _usb_error(usbmuxd, fake: FakeUsbmuxd) -> TransportError:
    async def work():
        with pytest.raises(TransportError) as caught:
            await connect(Transport(connect_timeout=15))
        return caught.value

    return usbmuxd(fake, work)


def test_a_locked_phone_over_the_os_usb_service_says_unlock(usbmuxd):
    fake = FakeUsbmuxd(pair_error="PasswordProtected")

    error = _usb_error(usbmuxd, fake)

    assert classify(error) == "locked"
    assert fake.requests[:1] == ["ReadBUID"]
    assert {"ListDevices", "Connect", "QueryType", "GetValue", "Pair"} <= set(fake.requests)


def test_dont_trust_over_the_os_usb_service_is_reported(usbmuxd):
    error = _usb_error(usbmuxd, FakeUsbmuxd(pair_error="UserDeniedPairing"))

    assert classify(error) == "trust_denied"


def test_no_phone_on_the_os_usb_service(usbmuxd):
    error = _usb_error(usbmuxd, FakeUsbmuxd(plugged_in=False))

    assert error.code == "no_usb_device"


def test_no_usb_service_at_all_names_this_os_service(monkeypatch, pymobiledevice3_home):
    if sys.platform == "win32":
        with socket.socket() as probe:
            if probe.connect_ex(WINDOWS_ADDRESS) == 0:
                pytest.skip("Apple Mobile Device Service runs on this computer")
        monkeypatch.delenv("USBMUXD_SOCKET_ADDRESS", raising=False)
    else:
        missing = os.path.join(tempfile.mkdtemp(prefix="mux", dir="/tmp"), "usbmuxd")
        monkeypatch.setenv("USBMUXD_SOCKET_ADDRESS", missing)

    with pytest.raises(TransportError) as caught:
        asyncio.run(connect(Transport(connect_timeout=15)))

    assert caught.value.code == "usbmuxd_unreachable"
    assert str(caught.value) == usb_service_help()[0]


@pytest.mark.skipif(not IN_CI, reason="talks to this computer's real USB service")
def test_the_real_usb_service_without_a_phone_gives_a_known_answer():
    """CI runners have no iPhone: Linux has no usbmuxd, Windows no Apple Mobile Device
    Service, macOS runs its own and finds no phone."""
    with pytest.raises(TransportError) as caught:
        asyncio.run(connect(Transport(connect_timeout=15)))

    print(f"{sys.platform}: {caught.value.code}: {caught.value}")
    assert caught.value.code in {"no_usb_device", "usbmuxd_unreachable"}


# ------------------------------------------------------------------ Wi-Fi on the real network stack

UDID = "00008120-0000WIFI0000FAKE"


def test_wifi_lookup_runs_on_this_os_network_stack(tmp_path, pymobiledevice3_home):
    """A RemotePairing record no phone will match: the Bonjour browse runs for real on
    this OS's interfaces and a remembered address refuses the connection; both must end
    in 'did not answer', not in a crash."""
    pytest.importorskip("pymobiledevice3.remote.tunnel_service")
    record = pymobiledevice3_home / f"remote_{UDID}.plist"
    record.write_bytes(plistlib.dumps({"peer_alt_irk": os.urandom(16)}))
    with socket.socket() as closed:
        closed.bind(("127.0.0.1", 0))
        port = closed.getsockname()[1]
    memory = AddressMemory(tmp_path / "addresses.json")
    memory.remember(UDID, "127.0.0.1", port)
    backend = PymobiledeviceBackend(memory)

    assert backend.remote_records() == [RemoteRecord(UDID, record, True)]
    assert asyncio.run(backend._browse(UDID, 1.0)) is None
    # The default connect budget: on a busy CI runner, starting and stopping Bonjour can
    # take longer than a tight budget, which would end in 'timeout' instead.
    with pytest.raises(TransportError) as caught:
        asyncio.run(connect(Transport(wifi=True, discovery_timeout=2), backend=backend))
    assert caught.value.code == "not_advertising"
