# Changelog

## Unreleased

- MCP server: `ios-homescreen mcp` lets Claude Desktop, Claude Code, Codex, Cursor, VS Code and other MCP clients read the home screen, plan changes and, after the person's explicit yes, write them. The tools are `find_phone`, `read_home_screen`, `list_apps`, `plan_layout`, `sort_pages`, `apply_layout`, `list_backups`, `plan_restore` and `restore_backup`; a write needs the id of a plan the server made and `confirm: true`, and goes through the same backup, read-back and automatic rollback as `push`. Works on Windows, macOS and Linux, from the command-line install (new `mcp` extra) or from the desktop app with no Python: `iconshuffle mcp` on macOS and Linux, `iconshuffle-mcp.exe` on Windows. `--demo` serves the pretend iPhone. Setup for each client is in [docs/mcp.md](docs/mcp.md).
- Only one write runs at a time: when the editor, `push`, `restore` or the MCP server is writing to the phone, another one stops with `busy` before it reads or writes anything.

## 0.4.0 — 2026-11-20

- The editor speaks eight languages: English, Turkish, German, Spanish, French, Japanese, Brazilian Portuguese and Simplified Chinese. It opens in the system language (English when none of them matches), a menu in the top bar switches it, and the choice is remembered. Buttons, dialogs, the change list, refusals, connection errors and progress messages are all translated; the command line, logs, the agent guide, error codes and the API stay English.
- The README is available in the same eight languages, with a language switcher at the top of each.

## 0.3.0 — 2026-11-20

- The repository is now github.com/YakupEmreYerli/IconShuffle; the old ios-homescreen address redirects to it, so existing installs and pinned links keep working. The command and the Python package stay `ios-homescreen`.
- A new glass logo for the app, the installers and the editor, with a simplified drawing for 16 and 32 px.
- The editor follows the system theme: lavender with frosted cards when it is light, the brand's deep ink with a violet glow when it is dark. Demo mode has lit icons like current iOS and a violet dusk wallpaper.
- One-line installers: `curl -fsSL https://iconshuffle.app/install.sh | sh` on macOS and Linux, `irm https://iconshuffle.app/install.ps1 | iex` on Windows. They install the latest desktop app from GitHub releases.
- Windows: a layout file saved with a byte order mark is read, and `check` or `push` no longer crash when their output goes to a pipe that is not UTF-8 (`--json` stays exact). Push keeps a file's CRLF line endings on every system.
- The command line's connection errors name the USB service of the system it runs on, not usbmuxd everywhere.
- The desktop app's `--self-test` runs one edit through its own server on the demo phone. [docs/platforms.md](docs/platforms.md) lists what is tested on each system and how beta testers can help.

## 0.2.0 — 2026-11-16

- IconShuffle: the product is now called IconShuffle — the desktop window, installers (`IconShuffle-*.exe`, `.dmg`, `.AppImage`), the editor's title bar and icons all carry the new name and the purple brand accent. The command and the Python package stay `ios-homescreen`.
- Sort A-Z: `ios-homescreen sort` rewrites the layout file with every page's apps, folders, web clips and web apps in name order, and the editor's Sort A-Z button does the same to the draft — the change list shows the moves and nothing reaches the phone until Apply. The dock, folder contents and widgets keep their places.
- Desktop app: `ios-homescreen-app` opens the editor in its own window, with no terminal or browser. It connects over USB when a cable is in and looks on the network otherwise. Downloadable builds for macOS (.dmg), Windows (installer .exe) and Linux (AppImage) are made by the Desktop apps workflow.
- macOS and Windows: data and cache go to the system's own folders, and the connection help names the service each system uses.

## 0.1.3 — 2026-11-13

- A layout with more than 15 pages is refused before anything is written: an iPhone keeps 15 pages and drops the rest, so such a write always rolled back. The editor's Add page stops at 15 too.
- Astronomy's watch proxy and Continuity are treated as hidden system services. They are not tagged hidden, but SpringBoard shows no icon for them, so placing them made a write roll back. They no longer show in the App Library list and cannot be placed.
- Both found by a contributor to [Rejig](https://github.com/rejig-app/rejig) on iOS 27.2 ([rejig-app/rejig#2](https://github.com/rejig-app/rejig/pull/2)).

## 0.1.2 — 2026-11-13

- A correct write is no longer rolled back when iOS moves a widget within its page to keep a nearly full page packed ([rejig-app/rejig#3](https://github.com/rejig-app/rejig/issues/3)), or puts a web clip that no read had shown into a slot the write freed ([rejig-app/rejig#7](https://github.com/rejig-app/rejig/issues/7)). Either case is reported as a warning; any other difference still rolls back.
- A second home screen icon of an installed app is called an extra icon, not a web app ([rejig-app/rejig#6](https://github.com/rejig-app/rejig/issues/6)).
- The Apply dialog, the README and the agent guide say that a write makes hidden pages visible again: the iPhone reads the same whether a page is hidden or not ([rejig-app/rejig#5](https://github.com/rejig-app/rejig/issues/5)).

## 0.1.1 — 2026-11-13

- Offloaded apps that live only in the App Library stay there after a write. Installation Proxy lists them only when asked for placeholders, so a write left them out of its ignored list and SpringBoard put them back on a page. An offloaded app moved to the home screen is now written in SpringBoard's own form. Found by [Rejig](https://github.com/rejig-app/rejig).
- Over Wi-Fi, a read that fails after a write opens a new tunnel to the same iPhone and tries once more: a home screen write can drop the whole tunnel. Found by Rejig.
- The Apply dialog, the Backups dialog and the README say that empty spaces between icons are not kept. Found by Rejig.
- Model names over USB for the iPhone 17e, iPhone 18 Pro, iPhone 18 Pro Max and iPhone Duo (#3).

## 0.1.0 — 2026-10-10

First release.

- Browser editor (`ios-homescreen editor`): a mirror of the phone with its real icons and widgets. Drag apps between pages, the dock and folders, make and rename folders, send apps to the App Library, undo and redo, see the list of changes, then Apply. `--demo` runs it against a pretend phone.
- AI agents: [`docs/agent-guide.md`](docs/agent-guide.md) and `llms.txt` tell a coding agent how to install and use the tool and to show the changes and wait for a yes before writing. A Claude Code skill in `skills/ios-homescreen`. `--json` output on every command and `ios-homescreen apps` to find an app and where it is.
- Safe writes: every write saves a backup first, reads the phone back and compares, and puts the backup back if the phone does not match. `backups` and `restore latest` undo a change.
- Command line: `pull` writes the layout to an editable TOML file, `check` shows what would change without touching the phone, `push` asks and writes.
- USB, and Wi-Fi without root: `wifi setup` once over USB, then the tool reaches the phone through a RemotePairing tunnel and remembers its address.
- Tested on an iPhone 15 with iOS 27.0.1 from Linux. Wi-Fi needs iOS 17 or later.
- Known limits: web clips and Safari web apps can only be deleted on the phone; a configurable widget may fall back to its default selection after a write; iOS 27 does not hand out the wallpaper over Wi-Fi.
