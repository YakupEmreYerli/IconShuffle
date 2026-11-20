<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <b>Español</b> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="Logo de IconShuffle: una pieza de cristal violeta que se levanta de su hueco">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>Reorganiza la pantalla de inicio de tu iPhone desde el ordenador.</b><br>
Arrastra tus iconos reales en un reflejo en directo de tu teléfono, o simplemente dile a tu agente de IA lo que quieres.<br>
Windows, macOS y Linux · USB o Wi-Fi · sin Mac, sin jailbreak, sin cuenta.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Descargar-Windows-8b6cff?logo=windows&logoColor=white" alt="Descargar para Windows"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Descargar-macOS-8b6cff?logo=apple&logoColor=white" alt="Descargar para macOS"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Descargar-Linux-8b6cff?logo=linux&logoColor=white" alt="Descargar para Linux"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/licencia-MIT-blue" alt="Licencia MIT"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Sitio web</a> · <a href="docs/agent-guide.md">Guía para agentes</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="Demo de IconShuffle: el editor refleja un iPhone de prueba; Ordenar A–Z reordena los iconos, la lista de cambios se va llenando y no se escribe nada hasta pulsar Aplicar">
</picture>

Ordenar sesenta iconos arrastrándolos uno a uno en una pantalla de seis pulgadas, mientras
tiemblan y se empujan unos a otros a la página siguiente, no le divierte a nadie. IconShuffle
lleva tu pantalla de inicio a la pantalla grande del ordenador, con tus iconos, carpetas y
widgets reales, y te deja organizarla ahí. Nada llega al teléfono hasta que pulsas Aplicar, y
cada escritura se respalda, se vuelve a leer y se deshace sola si el teléfono no coincide.

## Instalación

**Windows** (PowerShell):

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS y Linux:**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

Los scripts descargan la última versión de este repositorio y la instalan; léelos antes si
quieres: [`install.ps1`](install.ps1), [`install.sh`](install.sh). O descarga tú mismo el
instalador desde la [página de versiones](https://github.com/YakupEmreYerli/IconShuffle/releases/latest):
`IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg` o
`IconShuffle-*-linux-x86_64.AppImage`.

¿Prefieres la terminal? La herramienta de línea de comandos es un paquete de Python:

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# o
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

Las compilaciones todavía no están firmadas, así que la primera vez hace falta un clic más.
En macOS: Ajustes del Sistema → Privacidad y seguridad → **Abrir igualmente**. En Windows,
SmartScreen puede preguntar una vez: **Más información → Ejecutar de todas formas**.

## Tres formas de usarlo

**La app.** Abre IconShuffle y conecta tu iPhone. Verás tu pantalla de inicio con sus propios
iconos y su fondo de pantalla. Arrastra apps entre páginas y al Dock, suelta una app sobre
otra para crear una carpeta, trae apps desde la Biblioteca de apps o pulsa **Ordenar A–Z**.
A la derecha aparece cada cambio explicado con palabras sencillas; **Aplicar** los escribe.

**Tu agente de IA.** Claude Code, Codex, Cursor o cualquier agente de programación puede
hacerlo todo por ti. Pega esto, con tu propio deseo al final:

```text
Lee https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md y
ayúdame a reorganizar la pantalla de inicio de mi iPhone con ios-homescreen. Instálalo si
hace falta, enséñame cada cambio antes de escribir nada en el teléfono y espera a que te
diga que sí. Lo que quiero: pon mis apps del trabajo en una carpeta y mueve los juegos a la
página 2.
```

La [guía para agentes](docs/agent-guide.md) le explica al agente cómo instalar y manejar la
herramienta, y que debe enseñarte los cambios y esperar tu sí. Conectar el teléfono y tocar
Confiar sigue siendo cosa tuya. Claude Code también tiene un skill con el mismo flujo:
copia [`skills/ios-homescreen`](skills/ios-homescreen) en la carpeta `skills` dentro de
`~/.claude` (o dentro de la carpeta `.claude` de un proyecto).

Claude Desktop, Claude Code, Codex, Cursor, VS Code y otros clientes MCP también pueden
usar IconShuffle como **servidor MCP**, incluido en la app de escritorio (sin Python) y
en la herramienta de línea de comandos: [cómo configurarlo](docs/mcp.md) (en inglés), o
pruébalo sin teléfono en el modo demo.

**La terminal.** Tu disposición es un archivo TOML normal. Léela del teléfono, edítala en
cualquier editor y vuelve a escribirla:

```bash
ios-homescreen pull        # lee el teléfono en layout.toml (solo lectura)
ios-homescreen check       # muestra qué cambiaría (sin conexión)
ios-homescreen push        # pregunta, respalda, escribe, verifica, revierte si hace falta
```

## Seguro desde el diseño

El protocolo de la pantalla de inicio no está documentado y no perdona errores, así que
IconShuffle nunca se fía de una escritura que no puede comprobar:

- **Primero, una copia de seguridad.** Cada escritura guarda la disposición actual del
  teléfono antes de tocar nada.
- **Se vuelve a leer, siempre.** Después de escribir, el teléfono se lee de nuevo y se compara
  con el plan, icono por icono.
- **Se revierte solo.** Si el teléfono no coincide, la copia de seguridad se restaura
  automáticamente. `ios-homescreen restore latest` deshace cualquier escritura más adelante.
- **Pregunta antes de escribir.** Ves la lista completa de cambios y das tu sí, tanto si usas
  la app como la terminal o un agente.
- **Se queda en tu ordenador.** El editor solo escucha en 127.0.0.1; las disposiciones, los
  iconos y las copias de seguridad nunca salen de tu equipo. Sin cuenta y sin telemetría.

Los detalles están en [cómo funciona el modelo de seguridad](docs/reference.md#how-the-safety-model-works).

## Plataformas

| | Qué necesitas | Estado |
| --- | --- | --- |
| **Windows 10 y 11** (64 bits) | [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) de Microsoft Store (o iTunes): trae el controlador USB | Beta |
| **macOS** (Apple silicon) | Nada más | Beta |
| **Linux** | `usbmuxd`, instalado y en ejecución (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Estable |

El motor es el mismo en todos los sistemas y sus pruebas se ejecutan en los tres. Windows y
macOS están marcados como beta porque todavía no se han encontrado con muchos iPhone reales:
si pruebas IconShuffle en ellos, una [issue](https://github.com/YakupEmreYerli/IconShuffle/issues)
contando que funcionó (o que no) ayuda muchísimo. [docs/platforms.md](docs/platforms.md)
enumera lo que se prueba automáticamente en cada sistema.

En todos los sistemas: un iPhone que confíe en el ordenador (conéctalo una vez con un cable,
desbloquéalo, toca **Confiar en este ordenador** e introduce el código). El Wi-Fi funciona con
iOS 17 o posterior tras una configuración única por USB. Sin root y sin modo de desarrollador.

## Documentación

- [Referencia](docs/reference.md): todos los comandos y opciones, el archivo de disposición, el
  editor, [cómo funciona el modelo de seguridad](docs/reference.md#how-the-safety-model-works), Wi-Fi,
  archivos, la API de Python, limitaciones y solución de problemas.
- [Guía para agentes](docs/agent-guide.md): lo que necesita un agente de IA para manejar IconShuffle
  con seguridad.
- [Plataformas](docs/platforms.md): qué se prueba en cada sistema y cómo ayudar como beta tester.

## Contribuir y seguridad

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para la configuración, las pruebas y las trampas
que explican el diseño. Informa de los problemas de seguridad en privado, como se describe en
[SECURITY.md](SECURITY.md).

## Créditos

El payload de diccionario con una lista `ignored` sale de lo que descubrió la pull request #4
de [chungty/unjiggle](https://github.com/chungty/unjiggle) sobre `setIconState`. Las notas
sobre el formato del estado de los iconos en [facebook/idb](https://github.com/facebook/idb)
también ayudaron. No se copió código de ninguno de los dos proyectos.

La comunicación con el dispositivo pasa por [pymobiledevice3](https://github.com/doronz88/pymobiledevice3),
incluido su soporte de RemotePairing y su túnel en espacio de usuario para el Wi-Fi, y el
acceso USB por [usbmuxd](https://github.com/libimobiledevice/usbmuxd), del proyecto
libimobiledevice. El editor del navegador está hecho con [Preact](https://preactjs.com) y
[htm](https://github.com/developit/htm), y lo sirven [Starlette](https://www.starlette.io) y
[uvicorn](https://www.uvicorn.org).

## Licencia

[MIT](LICENSE). IconShuffle depende de pymobiledevice3, que tiene licencia GPL-3.0-or-later;
si distribuyes los dos juntos como un solo programa, esa combinación queda sujeta a la GPL.
El editor del navegador incluye copias sin modificar de Preact (MIT), htm (Apache-2.0) y la
fuente IBM Plex Sans (SIL Open Font License 1.1); sus licencias están a su lado, en
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) y
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts).
