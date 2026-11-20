"""The MCP server: its tools on fakes and the demo phone, and the real stdio process."""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import samples
from fakes import FakeSpringBoard
from ios_homescreen import desktop
from ios_homescreen.mcp_service import Refused, Service, Settings
from ios_homescreen.transport import TransportError
from ios_homescreen.workflow import Timing, WorkflowError, write_lock

mcp = pytest.importorskip("mcp")

FAST = Timing(read_timeout=5, write_timeout=5, verify_attempts=1, verify_interval=0)
ROOT = Path(__file__).resolve().parents[1]

READ_ONLY = {
    "find_phone",
    "read_home_screen",
    "list_apps",
    "plan_layout",
    "sort_pages",
    "list_backups",
    "plan_restore",
}
WRITES = {"apply_layout", "restore_backup"}


def run(coro):
    return asyncio.run(coro)


def fake_service(tmp_path, device=None, **settings):
    device = device or FakeSpringBoard(samples.home_screen(), samples.installed_apps())

    async def opener():
        return device

    config = Settings(data_dir=tmp_path, backup_dir=tmp_path / "backups", timing=FAST, **settings)
    return Service(config, opener=opener), device


def reversed_dock(service):
    read = run(service.read_home_screen())
    return {"dock": list(reversed(read["dock"])), "pages": read["pages"]}


# ------------------------------------------------------------------ reading never writes


def test_the_read_only_tools_never_write(tmp_path):
    service, device = fake_service(tmp_path)

    assert run(service.find_phone())["found"] is True
    read = run(service.read_home_screen(include_toml=True))
    run(service.list_apps("mail"))
    run(service.plan_layout(reversed_dock(service)))
    run(service.plan_layout(toml=read["toml"]))
    run(service.sort_pages())
    service.list_backups()

    assert device.writes == []
    assert not (tmp_path / "backups").exists()


def test_read_home_screen_returns_the_layout_and_the_saved_pull(tmp_path):
    service, _ = fake_service(tmp_path)

    read = run(service.read_home_screen(include_toml=True))

    assert read["summary"]["dock_items"] == 4
    assert read["summary"]["pages"] == 2
    assert [page["page"] for page in read["pages"]] == [1, 2]
    assert read["dock"][0]["type"] == "app"
    assert Path(read["pull_path"]).is_file()
    assert "[pull]" in read["toml"]
    assert json.dumps(read)


def test_list_apps_says_where_each_app_is(tmp_path):
    service, _ = fake_service(tmp_path)

    found = run(service.list_apps("com.apple.mobilemail"))["apps"]

    assert [app["id"] for app in found] == ["com.apple.mobilemail"]
    assert found[0]["where"]["section"] in {"dock", "page", "library"}


def test_find_phone_explains_what_to_do_when_there_is_none(tmp_path):
    async def nothing():
        raise TransportError("no iPhone found over USB", code="no_usb_device")

    service = Service(Settings(data_dir=tmp_path, backup_dir=tmp_path / "b"), opener=nothing)

    found = run(service.find_phone())

    assert found["found"] is False
    assert found["problem"]["code"] == "no_usb_device"
    assert "Trust" in found["next_step"]


def test_auto_connect_tries_usb_then_wifi_and_names_neither(tmp_path):
    class Nowhere:
        def __init__(self):
            self.tried = []

        async def usb(self, udid, pair_timeout):
            self.tried.append("usb")
            raise TransportError("no usb", code="no_usb_device")

        def remote_records(self):
            self.tried.append("wifi")
            return []

    backend = Nowhere()
    service = Service(
        Settings(data_dir=tmp_path, backup_dir=tmp_path / "b"),
        backend=backend,  # type: ignore[arg-type]
    )

    with pytest.raises(TransportError) as error:
        run(service._open())

    assert error.value.code == "no_device"
    assert backend.tried == ["usb", "wifi"]


# ------------------------------------------------------------------ planning


def test_a_valid_plan_lists_the_changes_and_gets_an_id(tmp_path):
    service, _ = fake_service(tmp_path)

    plan = run(service.plan_layout(reversed_dock(service)))

    assert plan["valid"] is True
    assert plan["unchanged"] is False
    assert len(plan["plan_id"]) == 16
    assert all(change["kind"] == "reordered" for change in plan["change_list"])
    assert plan["changes"]
    assert plan["summary"]
    assert "yes" in plan["next_step"]


def test_apps_by_name_and_bundle_id_plan(tmp_path):
    service, _ = fake_service(tmp_path)
    read = run(service.read_home_screen())
    layout = {"dock": ["com.apple.camera", "Safari"], "pages": read["pages"]}

    plan = run(service.plan_layout(layout))

    assert plan["valid"] is True, plan


def test_an_invalid_layout_returns_issues_and_no_plan(tmp_path):
    service, _ = fake_service(tmp_path)
    read = run(service.read_home_screen())

    plan = run(service.plan_layout({"dock": ["No Such App"], "pages": read["pages"]}))

    assert plan["valid"] is False
    assert plan["plan_id"] is None
    assert plan["issues"][0]["code"] == "unknown_app"
    assert service.pending == {}


def test_a_layout_of_the_wrong_shape_is_refused(tmp_path):
    service, _ = fake_service(tmp_path)

    with pytest.raises(Refused) as error:
        run(service.plan_layout({"dock": [], "pages": {"items": []}}))
    assert error.value.code == "bad_layout"
    with pytest.raises(Refused):
        run(service.plan_layout())


def test_an_unchanged_layout_has_nothing_to_apply(tmp_path):
    service, _ = fake_service(tmp_path)
    read = run(service.read_home_screen())

    plan = run(service.plan_layout({"dock": read["dock"], "pages": read["pages"]}))

    assert plan["unchanged"] is True
    assert plan["plan_id"] is None


def test_sort_pages_returns_the_sorted_layout_and_a_plan(tmp_path):
    service, _ = fake_service(tmp_path)

    plan = run(service.sort_pages())

    read = run(service.read_home_screen())
    assert plan["layout"]["dock"] == read["dock"]
    assert [len(p["items"]) for p in plan["layout"]["pages"]] == [
        len(p["items"]) for p in read["pages"]
    ]
    assert plan["plan_id"]
    assert {change["kind"] for change in plan["change_list"]} <= {"moved", "reordered"}


# ------------------------------------------------------------------ writing


def test_apply_writes_a_confirmed_plan_and_verifies_it(tmp_path):
    service, device = fake_service(tmp_path)
    layout = reversed_dock(service)
    plan = run(service.plan_layout(layout))

    result = run(service.apply_layout(plan["plan_id"], confirm=True))

    assert result["status"] == "applied"
    assert result["verified"] is True
    assert result["rolled_back"] is False
    assert (tmp_path / "backups" / result["backup"]).is_file()
    assert result["new_pull"]
    assert run(device.read_state())[0][0]["bundleIdentifier"] == layout["dock"][0]["id"]
    assert len(device.writes) == 1


def test_apply_refuses_without_confirm(tmp_path):
    service, device = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))

    for confirm in (False, "yes", 1):
        with pytest.raises(Refused) as error:
            run(service.apply_layout(plan["plan_id"], confirm=confirm))  # type: ignore[arg-type]
        assert error.value.code == "confirmation_needed"
    assert device.writes == []


def test_apply_refuses_a_plan_it_did_not_make(tmp_path):
    service, device = fake_service(tmp_path)
    run(service.plan_layout(reversed_dock(service)))

    with pytest.raises(Refused) as error:
        run(service.apply_layout("0123456789abcdef", confirm=True))

    assert error.value.code == "unknown_plan"
    assert device.writes == []


def test_a_plan_is_written_once(tmp_path):
    service, device = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))
    run(service.apply_layout(plan["plan_id"], confirm=True))

    with pytest.raises(Refused):
        run(service.apply_layout(plan["plan_id"], confirm=True))
    assert len(device.writes) == 1


def test_a_restore_plan_id_does_not_apply_a_layout(tmp_path):
    service, device = fake_service(tmp_path)
    first = run(service.plan_layout(reversed_dock(service)))
    run(service.apply_layout(first["plan_id"], confirm=True))
    restore = run(service.plan_restore("latest"))

    with pytest.raises(Refused):
        run(service.apply_layout(restore["plan_id"], confirm=True))
    assert len(device.writes) == 1


def test_a_write_the_phone_does_not_show_is_rolled_back(tmp_path):
    device = FakeSpringBoard(samples.home_screen(), samples.installed_apps(), ignore_writes=True)
    service, _ = fake_service(tmp_path, device)
    before = run(device.read_state())
    plan = run(service.plan_layout(reversed_dock(service)))

    result = run(service.apply_layout(plan["plan_id"], confirm=True))

    assert result["status"] == "rolled-back"
    assert result["rolled_back"] is True
    assert result["verified"] is False
    assert "as it was" in result["next_step"]
    assert len(device.writes) == 2  # the layout, then the backup
    assert run(device.read_state()) == before


def test_a_phone_changed_since_the_plan_is_not_written(tmp_path):
    service, device = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))
    device._state[1].reverse()  # someone rearranged page 1 on the phone

    with pytest.raises(WorkflowError) as error:
        run(service.apply_layout(plan["plan_id"], confirm=True))

    assert error.value.code == "layout_changed"
    assert device.writes == []


def test_a_write_elsewhere_makes_apply_busy_instead_of_racing_it(tmp_path):
    service, device = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))

    with write_lock(tmp_path / "backups"), pytest.raises(WorkflowError) as error:
        run(service.apply_layout(plan["plan_id"], confirm=True))

    assert error.value.code == "busy"
    assert device.writes == []
    assert list((tmp_path / "backups").glob("*.plist")) == []


def test_restore_plans_then_writes_after_confirm(tmp_path):
    service, device = fake_service(tmp_path)
    start = run(device.read_state())
    plan = run(service.plan_layout(reversed_dock(service)))
    run(service.apply_layout(plan["plan_id"], confirm=True))

    restore = run(service.plan_restore("latest"))
    assert restore["plan_id"]
    assert restore["changes"]
    assert len(device.writes) == 1
    with pytest.raises(Refused):
        run(service.restore_backup(restore["plan_id"]))
    result = run(service.restore_backup(restore["plan_id"], confirm=True))

    assert result["status"] == "applied"
    assert run(device.read_state())[0] == start[0]
    assert len(service.list_backups()["backups"]) == 2


def test_restore_refuses_once_the_phone_changed_after_the_plan(tmp_path):
    service, device = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))
    run(service.apply_layout(plan["plan_id"], confirm=True))
    restore = run(service.plan_restore("latest"))
    device._state[1].reverse()

    with pytest.raises(WorkflowError) as error:
        run(service.restore_backup(restore["plan_id"], confirm=True))

    assert error.value.code == "layout_changed"
    assert len(device.writes) == 1


def test_restore_refuses_another_iphones_backup_and_file_paths(tmp_path):
    service, _ = fake_service(tmp_path)
    plan = run(service.plan_layout(reversed_dock(service)))
    run(service.apply_layout(plan["plan_id"], confirm=True))
    other = FakeSpringBoard(
        samples.home_screen(), samples.installed_apps(), info={"name": "Other", "udid": "X"}
    )
    elsewhere, _ = fake_service(tmp_path, other)

    with pytest.raises(Refused) as error:
        run(elsewhere.plan_restore("latest"))
    assert error.value.code == "other_device"
    assert run(elsewhere.plan_restore("latest", allow_other_device=True))["backup"]
    backup = next((tmp_path / "backups").glob("*.plist"))
    with pytest.raises(Exception, match="no backup named"):
        run(service.plan_restore(str(backup)))


def test_the_demo_phone_takes_writes(tmp_path):
    service = Service.demo(tmp_path, delay=0)

    plan = run(service.sort_pages())
    result = run(service.apply_layout(plan["plan_id"], confirm=True))

    assert result["status"] == "applied"
    assert run(service.sort_pages())["unchanged"] is True
    assert run(service.find_phone())["connection"] == "demo"


# ------------------------------------------------------------------ the MCP layer


def call(client, name, arguments=None):
    return run_client(lambda c: c.call_tool(name, arguments or {}), client)


def run_client(work, service):
    from mcp import Client

    from ios_homescreen.mcp_server import build_server

    async def go():
        async with Client(build_server(service)) as client:
            return await work(client)

    return run(go())


def test_the_tools_are_annotated_as_reads_or_writes(tmp_path):
    tools = run_client(lambda c: c.list_tools(), Service.demo(tmp_path, delay=0)).tools

    by_name = {tool.name: tool for tool in tools}
    assert set(by_name) == READ_ONLY | WRITES
    for name in READ_ONLY:
        assert by_name[name].annotations.read_only_hint is True, name
    for name in WRITES:
        annotations = by_name[name].annotations
        assert annotations.read_only_hint is False
        assert annotations.destructive_hint is True
        assert "yes" in by_name[name].description
    assert all(tool.description for tool in tools)


def test_tool_errors_are_json_the_agent_can_act_on(tmp_path):
    service = Service.demo(tmp_path, delay=0)

    async def work(client):
        plan = await client.call_tool("sort_pages", {})
        refused = await client.call_tool(
            "apply_layout", {"plan_id": plan.structured_content["plan_id"]}
        )
        unknown = await client.call_tool("apply_layout", {"plan_id": "nope", "confirm": True})
        return refused, unknown

    refused, unknown = run_client(work, service)

    assert refused.is_error
    assert unknown.is_error
    text = refused.content[0].text
    error = json.loads(text[text.index("{") :])["error"]
    assert error["code"] == "confirmation_needed"
    assert '"unknown_plan"' in unknown.content[0].text


def test_the_prompt_explains_the_safe_flow(tmp_path):
    async def work(client):
        return await client.get_prompt("organize_home_screen", {"request": "games on page 2"})

    prompt = run_client(work, Service.demo(tmp_path, delay=0))

    text = prompt.messages[0].content.text
    assert "games on page 2" in text
    assert "apply_layout" in text
    assert "yes" in text


# ------------------------------------------------------------------ the real process


def _server_command(*args):
    return [sys.executable, "-m", "ios_homescreen", "mcp", "--demo", *args]


def test_end_to_end_over_stdio_with_the_sdk_client(tmp_path):
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters

    command = _server_command()
    env = {"IOS_HOMESCREEN_DATA_DIR": str(tmp_path / "data")}

    async def go():
        params = StdioServerParameters(command=command[0], args=command[1:], env=env)
        async with Client(params, read_timeout_seconds=60) as client:
            names = {tool.name for tool in (await client.list_tools()).tools}
            read = (await client.call_tool("read_home_screen", {})).structured_content
            layout = {"dock": list(reversed(read["dock"])), "pages": read["pages"]}
            plan = (await client.call_tool("plan_layout", {"layout": layout})).structured_content
            applied = await client.call_tool(
                "apply_layout", {"plan_id": plan["plan_id"], "confirm": True}
            )
            after = (await client.call_tool("read_home_screen", {})).structured_content
            return names, layout, applied.structured_content, after

    names, layout, applied, after = run(go())

    assert names == READ_ONLY | WRITES
    assert applied["status"] == "applied"
    assert [i["id"] for i in after["dock"]] == [i["id"] for i in layout["dock"]]
    # Demo mode keeps its files in a temporary folder, never the data directory.
    assert not (tmp_path / "data").exists()


def test_stdout_carries_only_the_protocol():
    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "read_home_screen", "arguments": {}},
        },
    ]
    text = "".join(json.dumps(m) + "\n" for m in messages)

    with subprocess.Popen(
        _server_command(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    ) as process:
        assert process.stdin
        assert process.stdout
        process.stdin.write(text.encode())
        process.stdin.flush()
        lines = []
        while len([line for line in lines if "id" in line]) < 3:
            raw = process.stdout.readline()
            assert raw, process.stderr.read().decode() if process.stderr else ""
            lines.append(json.loads(raw))
        process.stdin.close()
        rest = process.stdout.read().decode().splitlines()
        process.wait(timeout=30)

    for line in [*lines, *(json.loads(x) for x in rest if x.strip())]:
        assert line["jsonrpc"] == "2.0"
    answers = {line["id"]: line for line in lines if "id" in line}
    assert "result" in answers[1]
    assert "result" in answers[2]
    assert "result" in answers[3]


# ------------------------------------------------------------------ the desktop binary


def test_the_desktop_app_serves_mcp_when_asked(monkeypatch):
    seen = []
    monkeypatch.setattr("ios_homescreen.cli.main", lambda argv: seen.append(argv) or 0)

    assert desktop.main(["mcp", "--demo"]) == 0
    assert desktop.main(["--mcp"]) == 0
    assert seen == [["mcp", "--demo"], ["mcp"]]


def test_the_windows_console_twin_serves_mcp_without_being_told(monkeypatch, tmp_path):
    seen = []
    monkeypatch.setattr("ios_homescreen.cli.main", lambda argv: seen.append(argv) or 0)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "iconshuffle-mcp.exe"))

    assert desktop.main(["--demo"]) == 0
    assert seen == [["mcp", "--demo"]]


def test_a_windows_app_without_streams_hands_mcp_to_its_twin(monkeypatch, tmp_path):
    app = tmp_path / "iconshuffle.exe"
    (tmp_path / "iconshuffle-mcp.exe").write_bytes(b"")
    calls = []
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(sys, "executable", str(app))
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "stdout", None)
    monkeypatch.setattr(subprocess, "CREATE_NO_WINDOW", 0x08000000, raising=False)
    monkeypatch.setattr(subprocess, "call", lambda argv, **kw: calls.append((argv, kw)) or 5)

    assert desktop.main(["mcp", "--demo"]) == 5
    ((argv, options),) = calls
    assert argv == [str(tmp_path / "iconshuffle-mcp.exe"), "mcp", "--demo"]
    assert options["creationflags"] == 0x08000000
