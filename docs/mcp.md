# IconShuffle MCP server

IconShuffle can run as an [MCP](https://modelcontextprotocol.io) server, so an AI assistant
such as Claude Desktop, Claude Code, Codex, Cursor or VS Code can read your iPhone home
screen and rearrange it for you: "put the games on page 2", "make a Work folder", "sort my
pages A-Z". It works on Windows, macOS and Linux, from the downloaded app or from the
command-line install, over USB or Wi-Fi.

The assistant never writes on its own. It plans the change, shows you every move in plain
words and writes only after you say yes. Each write is backed up, read back from the phone
and rolled back automatically if the phone does not show it.

## What the assistant can do

| Tool | What it does | Writes to the phone |
| --- | --- | --- |
| `find_phone` | Finds the connected iPhone (USB first, then Wi-Fi) and says what to do if there is none | No |
| `read_home_screen` | Reads the dock, pages, folders, widgets, web clips and the App Library | No |
| `list_apps` | Lists the installed apps, their bundle ids and where each one is | No |
| `plan_layout` | Checks a new layout and lists what would change, in plain words | No |
| `sort_pages` | Plans every page A-Z, the same rules as the app's Sort A-Z | No |
| `apply_layout` | Writes a plan, only with its plan id and your confirmation | Yes |
| `list_backups` | Lists the backups made before every write | No |
| `plan_restore` | Lists what restoring a backup would change | No |
| `restore_backup` | Writes a backup back (undo), only with its plan id and your confirmation | Yes |

There is also an `organize_home_screen` prompt that walks the assistant through the safe
flow. Wi-Fi setup is not a tool yet: do it once in the app or with
`ios-homescreen wifi setup` over USB, and the server then finds the phone on the network
when no cable is in.

## Before you start

- The iPhone trusts this computer: connect it with a cable once, unlock it, tap **Trust
  This Computer** and enter the passcode.
- Windows: [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) from the
  Microsoft Store (or iTunes). Linux: `usbmuxd`, installed and running. macOS: nothing.

## Pick the command

Every client below starts the same server. Use the line for how you installed IconShuffle.

**Desktop app** (no Python needed). The app binary takes `mcp`:

| System | Command | Arguments |
| --- | --- | --- |
| Windows | `C:\Users\YOU\AppData\Local\Programs\IconShuffle\iconshuffle-mcp.exe` | none |
| macOS | `/Applications/IconShuffle.app/Contents/MacOS/iconshuffle` | `mcp` |
| Linux (install script) | `/home/YOU/.local/bin/iconshuffle` | `mcp` |
| Linux (AppImage elsewhere) | the path of `IconShuffle-*.AppImage` | `mcp` |

On Windows use `iconshuffle-mcp.exe`, which sits next to `iconshuffle.exe`: it is the same
program built as a console program, because MCP clients talk to the server through its
standard input and output, and a windowed program cannot be relied on for those.
`iconshuffle.exe mcp` also works; it hands over to `iconshuffle-mcp.exe` when it has to.
Replace `YOU` with your user name; MCP clients do not expand `~` or `%LOCALAPPDATA%`
everywhere, so write the full path.

**Command-line install with uv** (nothing to install first besides
[uv](https://docs.astral.sh/uv/)). `uvx` fetches IconShuffle with its MCP extra:

- Command: `uvx`
- Arguments: `--from`, `ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle`, `ios-homescreen`, `mcp`

**Already installed with pip, pipx or `uv tool install`:** add the extra
(`uv tool install 'ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle'`
or `pipx install 'ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle'`),
then the command is `ios-homescreen` with the argument `mcp`.

`ios-homescreen mcp` takes the usual options: `--udid UDID` to pick a phone, `--wifi` to
use only Wi-Fi, `--data-dir DIR` for the backups and snapshots. Run
`ios-homescreen mcp --help` for the list.

## Claude Desktop

Open the config file from Claude Desktop: **Settings → Developer → Edit Config**. It is
`claude_desktop_config.json` in:

- macOS: `~/Library/Application Support/Claude/`
- Windows: `%APPDATA%\Claude\`
- Linux (community builds): `~/.config/Claude/`

Add IconShuffle under `mcpServers`, then restart Claude Desktop.

macOS, desktop app:

```json
{
  "mcpServers": {
    "iconshuffle": {
      "command": "/Applications/IconShuffle.app/Contents/MacOS/iconshuffle",
      "args": ["mcp"]
    }
  }
}
```

Windows, desktop app (backslashes doubled in JSON):

```json
{
  "mcpServers": {
    "iconshuffle": {
      "command": "C:\\Users\\YOU\\AppData\\Local\\Programs\\IconShuffle\\iconshuffle-mcp.exe"
    }
  }
}
```

Any system, with uv:

```json
{
  "mcpServers": {
    "iconshuffle": {
      "command": "uvx",
      "args": [
        "--from",
        "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle",
        "ios-homescreen",
        "mcp"
      ]
    }
  }
}
```

If Claude Desktop cannot find `uvx`, give its full path (`which uvx` on macOS and Linux,
`where uvx` on Windows).

## Claude Code

```bash
# desktop app on macOS
claude mcp add iconshuffle -- /Applications/IconShuffle.app/Contents/MacOS/iconshuffle mcp
# or with uv, on any system
claude mcp add iconshuffle -- uvx --from "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle" ios-homescreen mcp
```

Add `--scope user` to have it in every project. `claude mcp list` shows whether it connects.

## Codex

```bash
codex mcp add iconshuffle -- uvx --from "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle" ios-homescreen mcp
```

Or in `~/.codex/config.toml`:

```toml
[mcp_servers.iconshuffle]
command = "uvx"
args = ["--from", "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle", "ios-homescreen", "mcp"]
# A write waits until the phone shows the new layout (up to about half a minute).
tool_timeout_sec = 120
```

With the desktop app, set `command` to the app's path and `args = ["mcp"]` (none for
`iconshuffle-mcp.exe`).

## Cursor

In `~/.cursor/mcp.json` (every project) or `.cursor/mcp.json` (one project):

```json
{
  "mcpServers": {
    "iconshuffle": {
      "command": "uvx",
      "args": [
        "--from",
        "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle",
        "ios-homescreen",
        "mcp"
      ]
    }
  }
}
```

## VS Code

In `.vscode/mcp.json`, or through **MCP: Add Server** in the command palette:

```json
{
  "servers": {
    "iconshuffle": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle",
        "ios-homescreen",
        "mcp"
      ]
    }
  }
}
```

For the desktop app in Cursor or VS Code, use its path as `command` and `["mcp"]` as
`args`, as in the Claude Desktop examples.

## Try it without a phone

Add `--demo` to the arguments and the server talks to the same pretend iPhone as the app's
demo mode: about fifty apps, folders, widgets, a web clip and an App Library. Every tool
works, including writes, which go to the pretend phone. Its backups and snapshots go to a
temporary folder that is deleted when the server stops, and nothing connects to a real
phone.

```bash
claude mcp add iconshuffle-demo -- uvx --from "ios-homescreen[mcp] @ git+https://github.com/YakupEmreYerli/IconShuffle" ios-homescreen mcp --demo
```

With the desktop app: `iconshuffle mcp --demo` (macOS, Linux) or
`iconshuffle-mcp.exe --demo` (Windows). Then ask the assistant something like "sort my
home screen A-Z" or "put the games on page 2".

## Safety

- **Nothing is written without your yes.** Planning tools never touch the phone's layout.
  `apply_layout` and `restore_backup` refuse unless they get the id of a plan this server
  made in this session and `confirm: true`, and their descriptions tell the assistant to
  show you the change list and wait for your explicit yes first. A plan is written at most
  once.
- **The same write path as the app and the command line.** A backup of the current layout
  first, then the write, then the phone is read back and compared with the plan; if it does
  not match, the backup is written back and checked too.
- **No surprises from elsewhere.** If the phone, the app or another tool changed the home
  screen after the plan was made, the write is refused and the assistant has to read and
  plan again. If the app or another command is writing at that moment, the server answers
  `busy` instead of writing over it.
- **Things that cannot be undone stay out of reach.** A layout that leaves out web clips or
  web apps is refused; removing widgets needs `allow_removal`, which the assistant is told
  to use only when you asked for it. Restores only take backups from the backup folder.
- **Local only.** The server talks to your MCP client over standard input and output and to
  the phone over USB or your local network. Layouts, icons and backups stay on your
  computer.

Undo any write with "restore the last backup": the assistant uses `plan_restore`, shows you
what changes, and calls `restore_backup` after your yes. `ios-homescreen restore latest`
does the same from a terminal.
