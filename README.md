<p align="center"><b>English</b> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="IconShuffle logo: a violet glass tile lifting out of its slot">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>Rearrange your iPhone home screen from your computer.</b><br>
Drag your real icons around a live mirror of your phone, or just tell your AI agent what you want.<br>
Windows, macOS and Linux · USB or Wi-Fi · no Mac, no jailbreak, no account.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Download-Windows-8b6cff?logo=windows&logoColor=white" alt="Download for Windows"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Download-macOS-8b6cff?logo=apple&logoColor=white" alt="Download for macOS"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Download-Linux-8b6cff?logo=linux&logoColor=white" alt="Download for Linux"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Website</a> · <a href="docs/agent-guide.md">Agent guide</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="IconShuffle demo: the editor mirrors a demo iPhone; Sort A-Z rearranges the icons, the change list fills in, and nothing is written until Apply is pressed">
</picture>

Sorting sixty icons by dragging them one by one on a six-inch screen, while they wiggle and
push each other onto the next page, is nobody's idea of fun. IconShuffle puts your home
screen on your computer's big screen, with your real icons, folders and widgets, and lets
you arrange it there. Nothing reaches the phone until you press Apply, and every write is
backed up, read back and undone on its own if the phone doesn't match.

## Install

**Windows** (PowerShell):

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS and Linux:**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

The scripts download the latest release from this repository and install it; read them
first if you like: [`install.ps1`](install.ps1), [`install.sh`](install.sh). Or grab the
installer yourself from the [releases page](https://github.com/YakupEmreYerli/IconShuffle/releases/latest):
`IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg` or
`IconShuffle-*-linux-x86_64.AppImage`.

Prefer the terminal? The command-line tool is a Python package:

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# or
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

The builds are not signed yet, so the first launch needs one extra click. On macOS:
System Settings → Privacy & Security → **Open Anyway**. On Windows, SmartScreen may ask
once: **More info → Run anyway**.

## Three ways to use it

**The app.** Open IconShuffle and plug in your iPhone. You see your home screen with its
own icons and wallpaper. Drag apps between pages and into the dock, drop one app on
another to make a folder, pull apps in from the App Library, or press **Sort A-Z**. The
right side lists every change in plain words; **Apply** writes them.

**Your AI agent.** Claude Code, Codex, Cursor or any coding agent can do the whole thing
for you. Paste this, with your own wish at the end:

```text
Read https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md and
help me rearrange my iPhone home screen with ios-homescreen. Install it if needed, show me
every change before anything is written to the phone, and wait for my yes. What I want:
put my work apps in one folder and move the games to page 2.
```

The [agent guide](docs/agent-guide.md) tells the agent how to install and drive the tool,
and that it must show you the changes and wait for your yes. You still plug in the phone
and tap Trust yourself. For Claude Code there is also a skill with the same workflow: copy
[`skills/ios-homescreen`](skills/ios-homescreen) into the `skills` folder inside `~/.claude`
(or inside a project's `.claude` folder).

**The terminal.** Your layout is a plain TOML file. Pull it, edit it in any editor, push it:

```bash
ios-homescreen pull        # read the phone into layout.toml (read-only)
ios-homescreen check       # see what would change (offline)
ios-homescreen push        # asks, backs up, writes, verifies, rolls back if needed
```

## Safe by design

The home screen protocol is undocumented and unforgiving, so IconShuffle never trusts a
write it cannot see:

- **A backup first.** Every write saves the phone's current layout before it touches anything.
- **Read back, every time.** After writing, the phone is read again and compared with the plan,
  icon by icon.
- **Rolls itself back.** If the phone doesn't match, the backup goes back on automatically.
  `ios-homescreen restore latest` undoes any write later.
- **Asks before it writes.** You see the full list of changes and say yes, whether you use the
  app, the terminal or an agent.
- **Stays on your computer.** The editor listens on 127.0.0.1 only; layouts, icons and backups
  never leave your machine. No account, no telemetry.

The details are in [how the safety model works](docs/reference.md#how-the-safety-model-works).

## Platforms

| | What you need | Status |
| --- | --- | --- |
| **Windows 10 and 11** (64-bit) | [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) from the Microsoft Store (or iTunes): it brings the USB driver | Beta |
| **macOS** (Apple silicon) | Nothing extra | Beta |
| **Linux** | `usbmuxd`, installed and running (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Stable |

The engine is the same on every system and its tests run on all three. Windows and macOS
are marked beta because they have not met many real iPhones yet: if you try IconShuffle
there, an [issue](https://github.com/YakupEmreYerli/IconShuffle/issues) saying it worked
(or didn't) helps a lot. [docs/platforms.md](docs/platforms.md) lists what is tested
automatically on each system.

On every system: an iPhone that trusts the computer (connect it with a cable once, unlock
it, tap **Trust This Computer** and enter the passcode). Wi-Fi works with iOS 17 and later
after a one-time setup over USB. No root, no Developer Mode.

## Documentation

- [Reference](docs/reference.md): every command and option, the layout file, the editor,
  [how the safety model works](docs/reference.md#how-the-safety-model-works), Wi-Fi, files,
  the Python API, limitations and troubleshooting.
- [Agent guide](docs/agent-guide.md): what an AI agent needs to drive IconShuffle safely.
- [Platforms](docs/platforms.md): what is tested on each system, and how to help as a beta tester.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests and the pitfalls behind the design.
Report security problems privately as described in [SECURITY.md](SECURITY.md).

## Credits

The dictionary payload with an `ignored` list comes from what
[chungty/unjiggle](https://github.com/chungty/unjiggle) pull request #4 found about
`setIconState`. The notes on the icon state format in [facebook/idb](https://github.com/facebook/idb)
helped too. No code was copied from either project.

Device communication goes through [pymobiledevice3](https://github.com/doronz88/pymobiledevice3),
including its RemotePairing support and userspace tunnel for Wi-Fi, and USB access through
[usbmuxd](https://github.com/libimobiledevice/usbmuxd) from the libimobiledevice project. The
browser editor is built with [Preact](https://preactjs.com) and [htm](https://github.com/developit/htm)
and served by [Starlette](https://www.starlette.io) and [uvicorn](https://www.uvicorn.org).

## License

[MIT](LICENSE). IconShuffle depends on pymobiledevice3, which is licensed GPL-3.0-or-later;
if you distribute the two together as one program, that combination falls under the GPL.
The browser editor ships unmodified copies of Preact (MIT), htm (Apache-2.0) and the IBM Plex
Sans font (SIL Open Font License 1.1); their licenses are next to them in
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) and
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts).
