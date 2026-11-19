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

<p align="center"><a href="https://iconshuffle.app">Website</a> · <a href="docs/agent-guide.md">Agent guide</a> · <a href="README.tr.md">Türkçe</a></p>

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

The details are in [How the safety model works](#how-the-safety-model-works).

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

## Features

- Reads the dock, pages, folders (including multi-page folders), widgets, widget stacks,
  web clips, Safari web apps and offloaded apps, and lists the apps that are only in the
  App Library.
- Shows what will move, what goes to the App Library and what comes back before anything
  is written.
- Checks a layout before it touches the phone: unknown or duplicate items, a full dock,
  pages over 24 cells (widgets count by size), empty or nested folders, widgets in folders.
- Apps you leave out go to the App Library and stay there.
- Sorts every page A-Z in one click, leaving the dock, folder contents and widgets in place.
- Refuses to write when the phone was changed since it was read.
- Has JSON output on every command, for scripts and agents, and a Python API
  (`ios_homescreen.api`) under the CLI.
- Keeps read snapshots and backups in its own data folder; only the layout file goes where
  you say.

The command is `ios-homescreen` and the Python package `ios_homescreen`: those names come
from the project's first months and stay, so existing scripts and tools built on it keep
working.

From a clone, for development:

```bash
git clone https://github.com/YakupEmreYerli/IconShuffle
cd IconShuffle
uv sync
uv run ios-homescreen --help
```

## Quick start

```bash
# 1. Read the phone into layout.toml. Read-only; nothing is written to the phone.
ios-homescreen pull

# 2. Edit it: move lines around, add apps from the list at the end, make folders.
$EDITOR layout.toml

# 3. See what would change. Offline.
ios-homescreen check

# 4. Write it. push shows the changes and asks; then backup, write, verify, roll back if needed.
ios-homescreen push
```

To undo a push, write back the backup it made:

```bash
ios-homescreen restore latest
```

## Commands

| Command | What it does | Talks to the phone |
| --- | --- | --- |
| `pull [LAYOUT]` | Reads the home screen into a layout file (`layout.toml` by default) and keeps the phone's state as a snapshot | Reads only |
| `check [LAYOUT]` | Checks the file and lists what `push` would change, compared with the pull | No |
| `sort [LAYOUT]` | Sorts every page's apps and folders A-Z in the file; the dock, folder contents and widgets keep their places | No |
| `push [LAYOUT]` | Shows the changes, asks, then backs up, writes, verifies and rolls back on failure | Writes |
| `apps [QUERY]` | Lists the installed apps with their bundle ids and where each one is, from the newest pull | No |
| `editor` | Opens the browser editor on 127.0.0.1 | Reads; writes only when you press Apply |
| `backups` | Lists the backups made before each write: when, which iPhone, what the layout held | No |
| `restore BACKUP` | Writes a backup back (`latest`, a name from `backups`, or a file), with the same steps as `push` | Writes |
| `wifi setup\|status\|off` | Sets up, checks or turns off Wi-Fi access to the phone | Yes |

`pull` will not replace a layout file that has edits you have not pushed; pull into another
file, or pass `--overwrite`. `check`, `sort` and `push` take `--allow-removal` (see the layout
reference); `push` and `restore` take `--force` (see the safety model). `backups` shows the 20
newest; `--all` lists every one. Every command except `wifi` takes `--data-dir DIR`;
`push`, `restore`, `editor` and `backups` also take `--backup-dir DIR`. All commands but
`editor` take `--json` and then print one JSON object on stdout, for scripts and agents;
the [agent guide](docs/agent-guide.md) describes it. With `--json`, `push` and `restore`
never ask: without `--yes` they only report what would change.

Connection options, for `pull`, `push`, `restore`, `editor` and `wifi`:

| Option | Meaning |
| --- | --- |
| *(none)* | USB through usbmuxd |
| `--wifi` | Wi-Fi (iOS 17 or later); run `wifi setup` over USB once first |
| `--udid UDID` | Pick a device when several are connected or paired |
| `--discovery-timeout SECONDS` | How long to listen for Bonjour answers (default 5) |
| `--connect-timeout SECONDS` | Time limit for opening the connection (default 30) |

Write options, for `push` and `restore` (and for `editor`, except `--yes`):

| Option | Meaning |
| --- | --- |
| `-y`, `--yes` | Write without asking. Needed when there is no terminal to ask in (scripts, pipes) |
| `--backup-dir DIR` | Where the automatic backup goes (default `DATA_DIR/backups`) |
| `--verify-attempts N` | Re-reads used to verify the write (default 6) |
| `--verify-interval SECONDS` | Pause between those re-reads (default 3) |
| `--write-timeout SECONDS` | Time limit for sending the layout (default 10) |
| `--read-timeout SECONDS` | Time limit for each read (default 30) |

Exit codes: `0` done (or nothing to do); `1` error, nothing was written (this includes a
phone that changed since the pull); `2` usage error, or the write was not confirmed (you
answered no, or there was no terminal and no `--yes`); `3` the new layout did not verify
and the backup was written back; `4` that did not verify either. The backup file is kept
in every case.

## Layout file

A layout has a `[dock]` table and one `[[pages]]` table per page, each with an `items`
array in home screen order: left to right, top to bottom.

```toml
[dock]
items = ["Phone", "Safari", "Messages", "Camera"]

[[pages]]
items = [
  { type = "widget", id = "6F1D3A52-0000-4000-8000-000000000001" },  # Weather, medium
  "com.apple.mobilecal",        # Calendar, by bundle id
  "Mail",                       # or by the name under the icon
  { type = "folder", name = "Utilities", items = ["Calculator", "Voice Memos", "Find My"] },
  { type = "folder", name = "Media", pages = [["Music", "Podcasts", "TV"], ["Books"]] },
  { type = "webclip", id = "0A1B2C3D4E5F40718293A4B5C6D7E8F9" },  # a Safari bookmark
  { type = "webapp", id = "9E8D7C6B-0000-4000-8000-000000000002" },  # a Safari web app
]

[[pages]]
items = ["Health", "Wallet"]
```

[`examples/layout.toml`](examples/layout.toml) is a complete example with Apple's stock apps.
Start from `pull` instead: it fills in your real ids, adds a comment with the name of every
item, and lists the apps that are only in the App Library at the end of the file, ready to
copy into a page.

The `[pull]` table at the top of a pulled file names the snapshot it came from
(`snapshot = "pull-....plist"` in `DATA_DIR/pulls`). `check` and `push` compare the file
with it; leave it as it is. A file without it is compared with the newest pull. After a
successful push, `push` saves the phone's new state and points the table at it, so the
file and the phone are in step again.

| Item | How to write it | Notes |
| --- | --- | --- |
| App | `"com.apple.Maps"` or `"Maps"` | A bundle id, or the app's name if only one app has it. `{ type = "app", id = "com.apple.Maps" }` also works and takes ids only. Any installed app can be added, including apps that are only in the App Library. |
| Folder | `{ type = "folder", name = "Work", items = [...] }` | `pages = [[...], [...]]` instead of `items` for a folder with several pages. Holds apps, web clips and web apps. |
| Widget or widget stack | `{ type = "widget", id = "..." }` | Small 4 cells, medium 8, large 16. Not allowed in the dock or in folders. |
| Web clip | `{ type = "webclip", id = "..." }` | A bookmark added with Add to Home Screen. Can be moved, not removed (see below). |
| Safari web app | `{ type = "webapp", id = "..." }` | A site added with Add to Home Screen and "Open as Web App" (iOS 26 and later). It has Safari's bundle id and its own id; it is a separate item from Safari. Can be moved, not removed. |
| Extra app icon | `{ type = "webapp", id = "..." }` | A second icon of an installed app: the app's bundle id with its own id. The layout file marks it `extra icon`. Can be moved, not removed. |

Rules the planner enforces:

- The dock holds at most 4 items. A page holds 24 cells; an app, folder, web clip or web app
  takes one.
- Each item appears once. Two widgets from the same app are different items with different ids.
- Folders need a name and at least one item, and cannot contain folders or widgets.
- Widgets, web clips and web apps can be moved, but a layout file cannot create them: they
  are referenced by the id they had in the pull, and the planner copies the phone's own data
  for them unchanged. Leaving out a widget is an error unless you pass `--allow-removal` to
  `check` and `push`.
- Web clips and Safari web apps cannot be removed by a write at all. When a written layout
  leaves one out, the phone puts it back on a new last page, the check after writing fails
  and the backup is restored. So the planner refuses such a layout (code `not_removable`),
  even with `--allow-removal`. Delete them on the phone (touch and hold, then Delete
  Bookmark), then `pull` again.
- Every installed app that is not in the layout goes to the App Library.
- Unknown keys are errors, so a typo such as `itmes` does not silently empty a page.

`check` (and `push`, before it connects) reports every problem it finds with its place, for
example `page 2, item 5: unknown app 'Mpas'`. What would change is listed in plain words:

```text
layout.toml is valid.
Changes compared with the pull from iPhone (iPhone 15, iOS 27.0) on 2026-10-10 14:44:

  Camera          moves from the dock to page 2, position 1
  Tips            comes from the App Library to page 2, position 2
  Folder "Tools"  was "Utilities"

1 moved, 1 added and 1 renamed.
30 apps will be only in the App Library.
```

## The editor

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/ui-dark.png">
<img src="docs/assets/ui-light.png" alt="The IconShuffle editor in demo mode after Sort A-Z: the App Library on the left, the phone in the middle, the list of changes and the Apply button on the right">
</picture>

The desktop app opens the editor in its own window; `ios-homescreen editor` opens the same
editor in your browser. It reads the phone and shows it with the
phone's app icons and, where the phone sends it, its wallpaper. Drag apps, folders and widgets around, between pages and
into the dock. Drop an app on another one to
make a folder; click a folder to open it, rename it, and drag apps in or out. The App
Library on the left lists the apps that are installed but not on the home screen: drag
them in, or drag apps there to take them off the home screen. The right side lists every
change compared with the last read and checks the layout with the same rules as `check`
while you edit.

Widgets show at their real size with their app's icon and name, and a stack shows how
many widgets it holds. The phone does not send what a widget displays, so the editor does
not make that up.

Apply asks for confirmation, then runs the same steps as `push`: backup, write, read back,
roll back if it does not match. The progress and the result show in the page. Backups lists
the automatic backups and restores one the same way. Import and Export load and save the
TOML layout file, so you can switch between the editor and a text editor; an exported file
works with `check` and `push`.

```bash
ios-homescreen editor          # over USB; add --wifi for Wi-Fi
ios-homescreen editor --demo   # a pretend iPhone with made-up apps
```

| Option | Meaning |
| --- | --- |
| `--port PORT` | Port on 127.0.0.1 (default: any free port) |
| `--no-browser` | Only print the address; do not open a browser |
| `--demo` | Use a pretend iPhone; nothing connects to a phone, and snapshots and backups go to a temporary folder |

The connection and write options work as for `push`. `--yes` is not needed: the editor asks.

The editor listens on 127.0.0.1 only. The address it prints contains a key that changes on
every start; the page trades it for a cookie, and every request has to carry the key and come
from the page itself, so other websites open in the same browser cannot use the editor or
see your icons, wallpaper and backups. Removing a widget needs its own confirmation, like
`--allow-removal`. Ctrl+Z and Ctrl+Shift+Z undo and redo.

## How the safety model works

The home screen protocol is undocumented, and two of its behaviours caused real damage while
this tool was being built. The design works around both.

1. The phone has to be told which apps to keep off the home screen. When `setIconState`
   receives only a list of pages, SpringBoard appends every installed app that is not on
   that list to the end of the home screen, App Library apps and Apple's stock apps
   included. IconShuffle always sends `{buttonBar, iconLists, ignored}`, where `ignored`
   lists every installed User and System app that is not on the home screen. It recomputes
   that list from the apps installed at the moment of writing.
2. A write gets no reliable answer. SpringBoard often never replies to `setIconState`, and
   pymobiledevice3's `set_icon_state` waits for that reply forever. IconShuffle sends the
   request itself with a time limit and treats a missing reply as "unknown". The proof is a
   fresh read of the phone that matches the plan.

Every `push` and `restore` runs the same steps:

1. Check the file offline, before connecting. A layout with problems never reaches the phone.
2. Connect and read the layout. `push` stops if it differs from the pull the file was made
   from (the phone was changed in the meantime); `--force` writes anyway. `restore` stops if
   the backup was made on another iPhone; `--force` restores it anyway.
3. Show what will change and ask. Only `y` or `yes` goes on. Without a terminal to ask in,
   the command needs `--yes`, and without it exits with code 2 before connecting.
4. Read the layout again and save it as a timestamped backup, with the iPhone's name and
   UDID. The phone-changed check runs again on this read.
5. Send the layout with a time limit.
6. Read the layout again on a new connection, up to `--verify-attempts` times, and compare it
   with what was sent: kinds, ids and order on every page and in every folder.
7. If it never matches, write the backup back the same way and verify that too.

Snapshots and backups are binary plists because the layout contains dates and binary data
that JSON would lose.

## Wi-Fi

Wi-Fi needs iOS 17 or later. Set it up once, with the phone connected over USB:

```bash
ios-homescreen wifi setup      # over USB, once
ios-homescreen wifi status     # the setting, the pairing, and whether the phone answers on Wi-Fi
```

`wifi setup` turns on the phone's Wi-Fi connections setting and pairs this computer for
Wi-Fi with RemotePairing, the mechanism Xcode uses for wireless devices. The computer is
already trusted over USB, so the phone shows no prompt. Root, Developer Mode and a tunnel
service are not needed: the connection runs through pymobiledevice3's userspace network stack
inside the IconShuffle process.

After that, add `--wifi` to `pull`, `push`, `restore` or `editor`. The phone must be on the same
network as the computer, awake and unlocked. IconShuffle looks for it with Bonjour
(`_remotepairing._tcp`) for `--discovery-timeout` seconds and recognises it by the pairing,
not by its address (iOS uses private, changing Wi-Fi addresses). If this computer is paired
with several phones, pass `--udid`.

Bonjour answers often go missing for a while even though the phone is listening. So after
every successful Wi-Fi connection IconShuffle remembers the address and port the phone
answered on, and next time it connects to that address directly while it browses, taking
whichever answers first. The addresses are kept in `wifi-addresses.json` in the cache
directory; deleting the file only makes the next connection rely on Bonjour.

The pairing is a file kept by pymobiledevice3: `~/.local/share/pymobiledevice3/remote_<UDID>.plist`,
or `~/.pymobiledevice3/` if that folder already exists. It holds the key that lets this
computer talk to the phone; IconShuffle never copies or sends it. `wifi off` turns the
phone's setting off, and `wifi off --forget` also deletes the pairing file.

The older way of reaching a phone over the network, lockdown on port 62078 found as
`_apple-mobdev2._tcp`, is not used: current iOS versions accept that connection but close
every service on the first request.

## Files and environment

The paths below are for Linux. On macOS the data and cache go under
`~/Library/Application Support/ios-homescreen` and `~/Library/Caches/ios-homescreen`; on
Windows under `%LOCALAPPDATA%\ios-homescreen`, with the cache in its `Cache` folder.

| What | Default | Override |
| --- | --- | --- |
| Pull snapshots and backups | `$XDG_DATA_HOME/ios-homescreen`, or `~/.local/share/ios-homescreen` | `--data-dir`, `IOS_HOMESCREEN_DATA_DIR` |
| App icons and wallpaper (browser editor), the phone's last Wi-Fi address | `$XDG_CACHE_HOME/ios-homescreen`, or `~/.cache/ios-homescreen` | `IOS_HOMESCREEN_CACHE_DIR` |
| Wi-Fi pairing (pymobiledevice3) | `$XDG_DATA_HOME/pymobiledevice3`, or `~/.local/share/pymobiledevice3` | `XDG_DATA_HOME` |

Inside the data directory: `pulls/pull-*.plist` (what `pull`, `push` and the editor read
from the phone) and `backups/backup-*.plist`. The only file written elsewhere is the layout
file `pull` writes: `layout.toml` in the current directory, or the path you give.

## Python API

```python
import asyncio
from ios_homescreen import api


async def main():
    device = await api.connect(api.Transport())  # api.Transport(wifi=True) for Wi-Fi
    try:
        snapshot = await api.read_device(device)  # what pull reads
        text = api.export_layout(snapshot)  # the TOML layout file
        plan = api.plan_layout(text, snapshot)  # what check does; raises api.LayoutError
        print(plan.changes)
        result = await api.push(
            device,
            plan,
            backup_dir=api.data_dir() / "backups",
            on_event=lambda event: print(event.message),
        )
        print(result.status)
    finally:
        await device.close()


asyncio.run(main())
```

Progress arrives as `Event` objects with a stable `code`; results and errors have `to_dict()`
and machine-readable codes. `api.describe(snapshot)` gives a JSON-ready view of a layout for a
UI and `api.to_document(view)` turns an edited view back into a layout; `plan.change_list`
holds the changes as data. `api.save_pull`, `api.list_backups`, `api.find_backup` and
`api.restore` work with the data directory like the CLI does, and `api.fetch_icons` returns
app icons as PNG bytes.

## Limitations

- Hidden home screen pages are read as normal pages, and a write makes them visible again:
  SpringBoard's read is the same whether a page is hidden or not (checked on iOS 27.2), so
  IconShuffle cannot tell them apart, keep them hidden, or hide a page.
- The Today view and Lock Screen widgets are not part of the home screen layout and are out
  of scope.
- Widgets can be moved or removed but not created. Web clips and Safari web apps can only be
  moved; delete them on the phone.
- Writing a layout can put widgets where you chose what they show, such as a stack's selected
  widget, back to their default choice: SpringBoard drops that choice on a write (seen on
  iOS 27). The check after writing ignores it for that reason.
- Empty spaces left between icons are not kept. SpringBoard sends each page as a list
  without cell positions, so a write can close gaps on any page, including pages you did not
  change (seen on iOS 26).
- Wi-Fi needs iOS 17 or later.
- The browser editor shows the phone's wallpaper only when SpringBoard sends it. On iOS 27
  over Wi-Fi the phone closes that request (seen on iOS 27.0.1), so the editor uses a plain
  background there. The only other way to get an image is a screenshot of the home screen
  with its icons, which cannot serve as a background.
- Empty pages are not written; SpringBoard does not keep them. An iPhone keeps at most 15
  pages, so a layout with more is refused before anything is written.
- Page capacity uses the iPhone grid (6 by 4). iPads have not been tested.
- The layout format is Apple's and undocumented, and an iOS update can change it. Pull again
  after an update; the backup and rollback are there for the case where it changes.
- The write format was verified on an iPhone 15 with iOS 26 and iOS 27.

## Troubleshooting

`no iPhone found over USB`: plug the phone in, unlock it, and check that usbmuxd is running
(`systemctl status usbmuxd`). On some distributions udev starts usbmuxd only when a device
appears.

A command hangs or every connection times out after an earlier session: usbmuxd sometimes
stops responding after a session. Restart it with `sudo systemctl restart usbmuxd` and
reconnect the phone.

`Mux error -8`, or a pairing error, on the first connection: the phone has not trusted this
computer yet. Unlock it, tap **Trust This Computer**, enter the passcode and run the command
again.

`the iPhone did not answer on the network`: check that the phone and the computer are on the
same network and that the phone is awake and unlocked; `wifi status` over USB shows whether it
answers. Guest networks and client isolation keep the two apart, and firewalls must allow mDNS
(UDP 5353).

`this computer has no Wi-Fi pairing yet`, or a pairing made by an older pymobiledevice3: run
`wifi setup` over USB again.

The browser says the page needs the address from the terminal: open the full address that
`ios-homescreen editor` printed. The key in it changes every time the editor starts.

`the iPhone's layout changed since layout.toml was pulled`: the phone was edited after your
`pull`. Pull into a new file (`ios-homescreen pull new.toml`), carry your edits over and push
that, or use `--force` if you want your file to win.

`there is no terminal to ask in`: `push` and `restore` ask before writing. In a script, add
`--yes` once you have checked the changes with `check`.

Exit code 3 (rolled back): the phone did not show the new layout in time. SpringBoard can be
slow, especially over Wi-Fi. Try `--verify-attempts 10 --verify-interval 5`.

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
