# Platforms

IconShuffle runs on Linux, macOS and Windows. Every push is tested on real Linux, macOS
and Windows machines in GitHub Actions, but those machines have no iPhone. The goal is
that the cable (or the Wi-Fi link) to a real iPhone is the only part left untested.

## What is verified automatically

| What | Linux | macOS | Windows | Where |
| --- | :-: | :-: | :-: | --- |
| Whole workflow (pull, edit, check, push, verify, rollback, restore) against a fake iPhone with names in several scripts | yes | yes | yes | `tests/test_platform.py`, `ci.yml` |
| Layout files saved by Windows editors (CRLF line endings, byte order mark) | yes | yes | yes | `tests/test_platform.py` |
| Output to a pipe that is not UTF-8 (`--json` stays exact) | yes | yes | yes | `tests/test_platform.py` |
| Data and cache folders | yes | yes | yes | `tests/test_paths_and_icons.py` |
| USB: pymobiledevice3 talks to a pretend usbmuxd at the OS's own address (a Unix socket; TCP 127.0.0.1:27015 on Windows, where Apple Mobile Device Service listens) and to a pretend phone behind it; a locked phone, "Don't Trust", no phone, no service | yes | yes | yes | `tests/test_platform.py`, `tests/fake_usbmuxd.py` |
| USB: the OS's real service with no phone gives a clear error | yes | yes | yes | `tests/test_platform.py` (CI only) |
| Error texts name this OS's USB service (usbmuxd, macOS, Apple Mobile Device Service) | yes | yes | yes | `tests/test_platform.py` |
| Wi-Fi: Bonjour lookup on the OS's real network stack, a remembered address that refuses | yes | yes | yes | `tests/test_platform.py` |
| Editor server: token, cookie, start and stop on 127.0.0.1 | yes | yes | yes | `tests/test_ui_server.py`, `tests/test_desktop.py` |
| Packaged app builds, and its self-test: page loads, one edit is read, applied and verified on the demo phone through the app's own server | yes | yes | yes | `apps.yml`, `smoke.yml` |
| MCP server: every tool on fakes and the demo phone, refusals, rollback, and a real stdio process driven by the SDK's client | yes | yes | yes | `tests/test_mcp.py` |
| Packaged app as an MCP server on the demo phone (`iconshuffle-mcp.exe` on Windows, the AppImage on Linux) | yes | yes | yes | `apps.yml` |
| Packaged app installs and its window opens (demo mode, screenshot) | yes | yes | yes | `smoke.yml` |
| One-line installers (`install.sh`, `install.ps1`) install the latest release and the app passes its self-test | yes | yes | yes | `installers.yml` |

## What is not verified

- **A real iPhone on macOS and Windows.** The USB cable through macOS's own usbmuxd or
  Windows' Apple Mobile Device Service, and the RemotePairing Wi-Fi link, have only been
  exercised against fakes there. On Linux they are used with a real iPhone.
- Trusting the computer on the phone, and the phone's own answers on those systems.
- Gatekeeper on a Mac that downloaded the app in a browser (the app is not signed yet).
- Intel Macs, 32-bit Windows and Linux on ARM: there are no builds for them.

## How to help as a beta tester

You need a Mac or a Windows PC, an iPhone and its cable. Everything below only **reads**
from the phone; nothing is written to it.

1. Install the app: `curl -fsSL https://iconshuffle.app/install.sh | sh` (Mac) or
   `irm https://iconshuffle.app/install.ps1 | iex` (PowerShell on Windows). On Windows,
   install Apple Devices from the Microsoft Store first (iTunes works too).
2. Plug in the iPhone, unlock it and tap **Trust** if it asks.
3. Open IconShuffle. It reads the home screen on its own. Check that it shows your
   pages. Do not press **Apply**.
4. If you also have [uv](https://docs.astral.sh/uv/), try the command line:

   ```
   uv tool install git+https://github.com/YakupEmreYerli/ios-homescreen
   ios-homescreen --version
   ios-homescreen pull test-layout.toml
   ios-homescreen check test-layout.toml
   ios-homescreen wifi status
   ```

   `pull` writes `test-layout.toml` and a snapshot on your computer only. If a command
   fails, run it again with `--json` and copy the `error` part.

Open an issue with:

- your system and version (for example macOS 15.5 on M2, or Windows 11 24H2),
- the iPhone model and iOS version,
- how you installed it and which steps worked,
- the exact error message or `error.code`, if any.

Please leave out app lists, screenshots of your home screen and your phone's name unless
you are happy for them to be public.
