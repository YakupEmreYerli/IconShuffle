<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <b>Deutsch</b> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="IconShuffle-Logo: eine violette Glaskachel, die sich aus ihrem Platz hebt">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>Ordne den Home-Bildschirm deines iPhones am Computer neu.</b><br>
Zieh deine echten Icons in einem Live-Spiegel deines iPhones herum oder sag einfach deinem KI-Agenten, was du willst.<br>
Windows, macOS und Linux · USB oder WLAN · kein Mac, kein Jailbreak, kein Konto.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Herunterladen-Windows-8b6cff?logo=windows&logoColor=white" alt="Für Windows herunterladen"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Herunterladen-macOS-8b6cff?logo=apple&logoColor=white" alt="Für macOS herunterladen"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Herunterladen-Linux-8b6cff?logo=linux&logoColor=white" alt="Für Linux herunterladen"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/Lizenz-MIT-blue" alt="MIT-Lizenz"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Website</a> · <a href="docs/agent-guide.md">Anleitung für Agenten</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="IconShuffle-Demo: Der Editor spiegelt ein Demo-iPhone; A–Z sortieren ordnet die Icons neu, die Liste der Änderungen füllt sich, und nichts wird geschrieben, bevor man auf Anwenden drückt">
</picture>

Sechzig Icons einzeln auf einem Sechs-Zoll-Bildschirm zu sortieren, während sie wackeln und
sich gegenseitig auf die nächste Seite schubsen, macht niemandem Spaß. IconShuffle holt deinen
Home-Bildschirm mit deinen echten Icons, Ordnern und Widgets auf den großen Bildschirm deines
Computers, und dort ordnest du ihn. Nichts landet auf dem iPhone, bevor du auf Anwenden drückst,
und jeder Schreibvorgang wird gesichert, zurückgelesen und von selbst rückgängig gemacht, wenn
das iPhone nicht dem Plan entspricht.

## Installation

**Windows** (PowerShell):

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS und Linux:**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

Die Skripte laden das neueste Release aus diesem Repository herunter und installieren es. Wenn
du willst, lies sie vorher: [`install.ps1`](install.ps1), [`install.sh`](install.sh). Oder hol
dir den Installer selbst von der [Releases-Seite](https://github.com/YakupEmreYerli/IconShuffle/releases/latest):
`IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg` oder
`IconShuffle-*-linux-x86_64.AppImage`.

Lieber im Terminal? Das Kommandozeilen-Tool ist ein Python-Paket:

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# oder
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

Die Builds sind noch nicht signiert, deshalb braucht der erste Start einen zusätzlichen Klick.
Unter macOS: Systemeinstellungen → Datenschutz & Sicherheit → **Dennoch öffnen**. Unter Windows
fragt SmartScreen eventuell einmal nach: **Weitere Informationen → Trotzdem ausführen**.

## Drei Wege, es zu nutzen

**Die App.** Öffne IconShuffle und schließ dein iPhone an. Du siehst deinen Home-Bildschirm
mit seinen eigenen Icons und seinem Hintergrundbild. Zieh Apps zwischen Seiten und ins Dock,
leg eine App auf eine andere, um einen Ordner zu erstellen, hol Apps aus der App-Mediathek
oder drück **A–Z sortieren**. Rechts steht jede Änderung in einfachen Worten; **Anwenden**
schreibt sie.

**Dein KI-Agent.** Claude Code, Codex, Cursor oder jeder andere Coding-Agent kann das Ganze
für dich erledigen. Füg das hier ein und schreib deinen eigenen Wunsch ans Ende:

```text
Lies https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md und
hilf mir, den Home-Bildschirm meines iPhones mit ios-homescreen neu zu ordnen. Installier
es, falls nötig, zeig mir jede Änderung, bevor etwas auf das iPhone geschrieben wird, und
warte auf mein Ja. Was ich will: Leg meine Arbeits-Apps in einen Ordner und verschieb die
Spiele auf Seite 2.
```

Die [Anleitung für Agenten](docs/agent-guide.md) erklärt dem Agenten, wie er das Tool
installiert und bedient, und dass er dir die Änderungen zeigen und auf dein Ja warten muss.
Das iPhone anschließen und auf „Vertrauen“ tippen musst du weiterhin selbst. Für Claude Code
gibt es außerdem einen Skill mit demselben Ablauf: Kopier
[`skills/ios-homescreen`](skills/ios-homescreen) in den Ordner `skills` in `~/.claude`
(oder in den `.claude`-Ordner eines Projekts).

Claude Desktop, Claude Code, Codex, Cursor, VS Code und andere MCP-Clients können
IconShuffle auch als **MCP-Server** nutzen. Er steckt in der Desktop-App (kein Python
nötig) und im Kommandozeilen-Tool: [so richten Sie ihn ein](docs/mcp.md) (Englisch),
oder probieren Sie ihn im Demo-Modus ohne iPhone aus.

**Das Terminal.** Dein Layout ist eine einfache TOML-Datei. Lies sie aus, bearbeite sie in
einem beliebigen Editor und schreib sie zurück:

```bash
ios-homescreen pull        # iPhone in layout.toml einlesen (nur lesen)
ios-homescreen check       # sehen, was sich ändern würde (offline)
ios-homescreen push        # fragt, sichert, schreibt, prüft, macht bei Bedarf rückgängig
```

## Von Grund auf sicher

Das Protokoll für den Home-Bildschirm ist nicht dokumentiert und verzeiht keine Fehler.
Deshalb vertraut IconShuffle keinem Schreibvorgang, den es nicht überprüfen kann:

- **Zuerst ein Backup.** Jeder Schreibvorgang speichert das aktuelle Layout des iPhones,
  bevor er irgendetwas anfasst.
- **Jedes Mal zurückgelesen.** Nach dem Schreiben wird das iPhone erneut ausgelesen und Icon
  für Icon mit dem Plan verglichen.
- **Macht sich selbst rückgängig.** Passt das iPhone nicht, wird das Backup automatisch
  wiederhergestellt. `ios-homescreen restore latest` macht jeden Schreibvorgang auch später
  noch rückgängig.
- **Fragt, bevor es schreibt.** Du siehst die komplette Liste der Änderungen und sagst Ja,
  egal ob du die App, das Terminal oder einen Agenten nutzt.
- **Bleibt auf deinem Computer.** Der Editor lauscht nur auf 127.0.0.1; Layouts, Icons und
  Backups verlassen nie deinen Rechner. Kein Konto, keine Telemetrie.

Die Details stehen unter [So funktioniert das Sicherheitsmodell](docs/reference.md#how-the-safety-model-works).

## Plattformen

| | Was du brauchst | Status |
| --- | --- | --- |
| **Windows 10 und 11** (64 Bit) | [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) aus dem Microsoft Store (oder iTunes): Es bringt den USB-Treiber mit | Beta |
| **macOS** (Apple Silicon) | Nichts weiter | Beta |
| **Linux** | `usbmuxd`, installiert und laufend (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Stabil |

Die Engine ist auf jedem System dieselbe, und ihre Tests laufen auf allen dreien. Windows und
macOS sind als Beta markiert, weil sie noch nicht vielen echten iPhones begegnet sind. Eine
Person hat die macOS-App per USB mit einem iPhone 15 Pro benutzt und aufgeschrieben, was
funktioniert hat ([Issue #6](https://github.com/YakupEmreYerli/IconShuffle/issues/6)); ein
Bericht von dir hilft genauso. [docs/platforms.md](docs/platforms.md) listet auf, was auf
jedem System automatisch getestet wird.

Auf jedem System gilt: Das iPhone muss dem Computer vertrauen (einmal per Kabel verbinden,
entsperren, auf **Diesem Computer vertrauen** tippen und den Code eingeben). WLAN funktioniert
ab iOS 17 nach einer einmaligen Einrichtung über USB. Kein Root, kein Entwicklermodus.

## Dokumentation

- [Referenz](docs/reference.md): alle Befehle und Optionen, die Layout-Datei, der Editor,
  [so funktioniert das Sicherheitsmodell](docs/reference.md#how-the-safety-model-works), WLAN, Dateien,
  die Python-API, Einschränkungen und Fehlerbehebung.
- [Anleitung für Agenten](docs/agent-guide.md): was ein KI-Agent braucht, um IconShuffle sicher zu bedienen.
- [Plattformen](docs/platforms.md): was auf jedem System getestet wird und wie du als Beta-Tester
  helfen kannst.

## Mitmachen und Sicherheit

In [CONTRIBUTING.md](CONTRIBUTING.md) findest du Einrichtung, Tests und die Stolperfallen
hinter dem Design. Sicherheitsprobleme meldest du vertraulich, wie in [SECURITY.md](SECURITY.md)
beschrieben.

## Danksagung

Der Dictionary-Payload mit einer `ignored`-Liste geht auf das zurück, was Pull Request #4 von
[chungty/unjiggle](https://github.com/chungty/unjiggle) über `setIconState` herausgefunden hat.
Auch die Notizen zum Icon-State-Format in [facebook/idb](https://github.com/facebook/idb)
haben geholfen. Aus keinem der beiden Projekte wurde Code kopiert.

Die Kommunikation mit dem Gerät läuft über [pymobiledevice3](https://github.com/doronz88/pymobiledevice3),
einschließlich seiner RemotePairing-Unterstützung und des Userspace-Tunnels für WLAN, der
USB-Zugriff über [usbmuxd](https://github.com/libimobiledevice/usbmuxd) aus dem
libimobiledevice-Projekt. Der Browser-Editor ist mit [Preact](https://preactjs.com) und
[htm](https://github.com/developit/htm) gebaut und wird von [Starlette](https://www.starlette.io)
und [uvicorn](https://www.uvicorn.org) ausgeliefert.

## Lizenz

[MIT](LICENSE). IconShuffle hängt von pymobiledevice3 ab, das unter GPL-3.0-or-later steht;
wenn du beide zusammen als ein Programm weitergibst, fällt diese Kombination unter die GPL.
Der Browser-Editor enthält unveränderte Kopien von Preact (MIT), htm (Apache-2.0) und der
Schrift IBM Plex Sans (SIL Open Font License 1.1); ihre Lizenzen liegen daneben in
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) und
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts).
