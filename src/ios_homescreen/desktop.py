"""The desktop app: the browser editor in its own window, without a terminal.

It runs the same server as ``ios-homescreen editor`` on a free local port, in a
background thread, and shows the page in a pywebview window (WebKit on macOS, WebView2
on Windows, Qt on Linux). Closing the window stops the server. Nobody picks USB or
Wi-Fi here, so the app tries USB first and the network when no cable is in.
"""

from __future__ import annotations

import html
import json
import re
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from . import __version__
from .paths import BACKUPS, data_dir
from .transport import Transport
from .ui import Options, serve
from .workflow import Timing

TITLE = "IconShuffle"
START_TIMEOUT = 30.0
ICON = Path(__file__).parent / "ui" / "static" / "logo.png"


def _window_icon() -> str | None:
    """The window icon on Linux; macOS and Windows take it from the app bundle, and
    WinForms' ``Icon`` refuses the PNG with an ArgumentException before the window shows."""
    return str(ICON) if sys.platform == "linux" else None


def _options(demo: bool) -> Options:
    data = data_dir()
    return Options(
        transport=Transport(),
        data_dir=data,
        backup_dir=data / BACKUPS,
        timing=Timing(),
        open_browser=False,
        demo=demo,
        auto=True,
    )


def _self_test() -> int:
    """For the build pipeline: start the server in demo mode, load the page, run one edit
    through it (read, apply, verify on the pretend iPhone), stop.

    It also imports the window backend, so a package that lost it fails here.
    """
    import http.cookiejar
    import urllib.request

    import webview  # noqa: F401

    started = threading.Event()
    found: dict[str, object] = {}

    def on_started(url: str, stop: Callable[[], None]) -> None:
        found["url"], found["stop"] = url, stop
        started.set()

    thread = threading.Thread(
        target=serve,
        args=(_options(demo=True),),
        kwargs={"say": lambda _text: None, "on_started": on_started},
        daemon=True,
    )
    thread.start()
    if not started.wait(START_TIMEOUT):
        print("self-test: the editor did not start")
        return 1
    # The address carries a one-time token that the server swaps for a cookie.
    browser = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )
    url = str(found["url"])
    try:
        with browser.open(url, timeout=10) as page:
            body = page.read()
            problem = None if page.status == 200 and b"IconShuffle" in body else "no page"
        problem = problem or _round_trip(browser, url.split("/?", 1)[0], body)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        problem = f"{type(exc).__name__}: {exc}"
    stop = found["stop"]
    assert callable(stop)
    stop()
    thread.join(timeout=10)
    print(f"self-test: {problem or 'ok'} ({__version__})")
    return 0 if problem is None else 1


def _round_trip(browser: Any, base: str, page: bytes) -> str | None:
    """What the page does for one edit: wait for the first read, reverse the dock, apply,
    and see the phone show it. Returns what went wrong, or ``None``."""
    import urllib.request

    token = re.search(rb'name="ihs-token" content="([^"]+)"', page)
    if token is None:
        return "the page has no token"
    headers = {"X-IHS-Token": token.group(1).decode(), "Origin": base}

    def call(path: str, body: Any = None) -> Any:
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(base + path, data=data, headers=headers)
        if data is not None:
            request.add_header("Content-Type", "application/json")
        with browser.open(request, timeout=10) as answer:
            return json.loads(answer.read())

    def finished() -> dict[str, Any] | None:
        deadline = time.monotonic() + START_TIMEOUT
        while time.monotonic() < deadline:
            job = call("/api/job")["job"]
            if job and job["state"] != "running":
                return job
            time.sleep(0.1)
        return None

    if (finished() or {}).get("state") != "done":
        return "the first read did not finish"
    view = call("/api/state")["read"]["view"]
    dock = [item["id"] for item in reversed(view["dock"])]
    layout = {
        "dock": list(reversed(view["dock"])),
        "pages": [{"items": page["items"]} for page in view["pages"]],
    }
    call("/api/apply", {"layout": layout})
    job = finished() or {}
    if (job.get("result") or {}).get("status") != "applied":
        return f"the edit was not applied: {job.get('error') or job.get('result')}"
    if [item["id"] for item in call("/api/state")["read"]["view"]["dock"]] != dock:
        return "the phone does not show the edit"
    return None


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--self-test" in args:
        return _self_test()

    import webview

    started = threading.Event()
    found: dict[str, object] = {}

    def on_started(url: str, stop: Callable[[], None]) -> None:
        found["url"], found["stop"] = url, stop
        started.set()

    def run() -> None:
        try:
            serve(_options("--demo" in args), say=lambda _text: None, on_started=on_started)
        except BaseException as exc:  # shown in the window instead of a lost traceback
            found["error"] = exc
            started.set()

    server = threading.Thread(target=run, name="ios-homescreen-server", daemon=True)
    server.start()
    if not started.wait(START_TIMEOUT) or "error" in found:
        message = str(found.get("error") or "the editor did not start")
        page = f"<p>IconShuffle could not start: {html.escape(message)}</p>"
        webview.create_window(TITLE, html=page)
        webview.start()
        return 1

    webview.create_window(
        f"{TITLE} {__version__}",
        str(found["url"]),
        width=1280,
        height=820,
        min_size=(900, 600),
    )
    try:
        webview.start(icon=_window_icon())
    finally:
        stop = found["stop"]
        assert callable(stop)
        stop()
        server.join(timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
