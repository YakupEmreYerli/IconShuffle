<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <b>Português (Brasil)</b> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="Logo do IconShuffle: um bloco de vidro violeta saindo do seu encaixe">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>Organize a tela inicial do seu iPhone pelo computador.</b><br>
Arraste seus ícones reais num espelho ao vivo do celular, ou simplesmente diga ao seu agente de IA o que você quer.<br>
Windows, macOS e Linux · USB ou Wi-Fi · sem Mac, sem jailbreak, sem conta.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Baixar-Windows-8b6cff?logo=windows&logoColor=white" alt="Baixar para Windows"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Baixar-macOS-8b6cff?logo=apple&logoColor=white" alt="Baixar para macOS"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/Baixar-Linux-8b6cff?logo=linux&logoColor=white" alt="Baixar para Linux"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/licen%C3%A7a-MIT-blue" alt="Licença MIT"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Site</a> · <a href="docs/agent-guide.md">Guia para agentes</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="Demonstração do IconShuffle: o editor espelha um iPhone de demonstração; Ordenar A–Z reorganiza os ícones, a lista de mudanças vai se enchendo e nada é gravado até você clicar em Aplicar">
</picture>

Ninguém gosta de arrastar sessenta ícones um por um numa tela de seis polegadas, com eles
tremendo e empurrando uns aos outros para a página seguinte. O IconShuffle leva a sua tela
inicial para a tela grande do computador, com seus ícones, pastas e widgets reais, e deixa
você organizar tudo por lá. Nada chega ao celular até você clicar em Aplicar, e cada gravação
tem backup, é conferida lendo o celular de novo e se desfaz sozinha se o resultado não bater.

## Instalação

**Windows** (PowerShell):

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS e Linux:**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

Os scripts baixam a versão mais recente deste repositório e fazem a instalação; se quiser,
leia antes: [`install.ps1`](install.ps1), [`install.sh`](install.sh). Ou baixe você mesmo o
instalador na [página de versões](https://github.com/YakupEmreYerli/IconShuffle/releases/latest):
`IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg` ou
`IconShuffle-*-linux-x86_64.AppImage`.

Prefere o terminal? A ferramenta de linha de comando é um pacote Python:

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# ou
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

Os instaladores ainda não são assinados, então a primeira abertura pede um clique a mais. No
macOS: Ajustes do Sistema → Privacidade e Segurança → **Abrir Mesmo Assim**. No Windows, o
SmartScreen pode perguntar uma vez: **Mais informações → Executar assim mesmo**.

## Três jeitos de usar

**O app.** Abra o IconShuffle e conecte o iPhone. Você vê a sua tela inicial com os próprios
ícones e o papel de parede. Arraste apps entre as páginas e para o Dock, solte um app em cima
de outro para criar uma pasta, puxe apps da Biblioteca de Apps ou clique em **Ordenar A–Z**. O
lado direito lista cada mudança em palavras simples; **Aplicar** grava tudo.

**Seu agente de IA.** Claude Code, Codex, Cursor ou qualquer agente de programação pode fazer
o trabalho todo por você. Cole isto, com o seu pedido no final:

```text
Leia https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md e me
ajude a organizar a tela inicial do meu iPhone com o iconshuffle. Instale se precisar,
me mostre cada mudança antes de gravar qualquer coisa no celular e espere o meu sim. O que
eu quero: colocar meus apps de trabalho numa pasta e mover os jogos para a página 2.
```

O [guia para agentes](docs/agent-guide.md) explica ao agente como instalar e usar a
ferramenta, e que ele precisa mostrar as mudanças e esperar o seu sim. Conectar o celular e
tocar em Confiar continua sendo com você. O Claude Code também tem uma skill com o
mesmo fluxo: copie [`skills/iconshuffle`](skills/iconshuffle) para a pasta `skills`
dentro de `~/.claude` (ou dentro da pasta `.claude` de um projeto).

Claude Desktop, Claude Code, Codex, Cursor, VS Code e outros clientes MCP também podem
usar o IconShuffle como **servidor MCP**, que vem no app para desktop (sem Python) e na
ferramenta de linha de comando: [veja como configurar](docs/mcp.md) (em inglês), ou
experimente sem celular no modo demo.

**O terminal.** O seu layout é um arquivo TOML simples. Puxe, edite em qualquer editor e envie:

```bash
iconshuffle pull        # lê o celular para o layout.toml (só leitura)
iconshuffle check       # mostra o que mudaria (offline)
iconshuffle push        # pergunta, faz backup, grava, confere e desfaz se precisar
```

## Seguro por padrão

O protocolo da tela inicial não é documentado e não perdoa erros, então o IconShuffle nunca
confia numa gravação que não consegue ver:

- **Backup primeiro.** Toda gravação salva o layout atual do celular antes de mexer em qualquer coisa.
- **Confere toda vez.** Depois de gravar, o celular é lido de novo e comparado com o plano,
  ícone por ícone.
- **Desfaz sozinho.** Se o celular não bater com o plano, o backup volta automaticamente.
  `iconshuffle restore latest` desfaz qualquer gravação depois.
- **Pergunta antes de gravar.** Você vê a lista completa de mudanças e dá o seu sim, seja no
  app, no terminal ou com um agente.
- **Fica no seu computador.** O editor só escuta em 127.0.0.1; layouts, ícones e backups
  nunca saem da sua máquina. Sem conta, sem telemetria.

Os detalhes estão em [como funciona o modelo de segurança](docs/reference.md#how-the-safety-model-works).

## Plataformas

| | O que você precisa | Status |
| --- | --- | --- |
| **Windows 10 e 11** (64 bits) | [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) da Microsoft Store (ou iTunes): ele traz o driver USB | Beta |
| **macOS** (Apple silicon) | Nada a mais | Beta |
| **Linux** | `usbmuxd` instalado e em execução (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Estável |

O motor é o mesmo em todos os sistemas e os testes rodam nos três. Windows e macOS estão
marcados como beta porque ainda não passaram por muitos iPhones de verdade. Uma pessoa usou
o app do macOS por USB com um iPhone 15 Pro e contou o que funcionou
([issue #6](https://github.com/YakupEmreYerli/IconShuffle/issues/6)); o seu teste ajuda do
mesmo jeito. [docs/platforms.md](docs/platforms.md) lista o que é testado automaticamente
em cada sistema.

Em qualquer sistema: um iPhone que confie no computador (conecte com um cabo uma vez,
desbloqueie, toque em **Confiar Neste Computador** e digite o código). O Wi-Fi funciona no
iOS 17 ou mais recente depois de uma configuração única por USB. Sem root, sem Modo de
Desenvolvedor.

## Documentação

- [Referência](docs/reference.md): todos os comandos e opções, o arquivo de layout, o editor,
  [como funciona o modelo de segurança](docs/reference.md#how-the-safety-model-works), Wi-Fi,
  arquivos, a API Python, limitações e solução de problemas.
- [Guia para agentes](docs/agent-guide.md): o que um agente de IA precisa para usar o
  IconShuffle com segurança.
- [Plataformas](docs/platforms.md): o que é testado em cada sistema e como ajudar como testador beta.

## Contribuição e segurança

Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para configuração, testes e as armadilhas por trás
do design. Relate problemas de segurança em particular, como descrito no [SECURITY.md](SECURITY.md).

## Créditos

O payload em dicionário com uma lista `ignored` vem do que o pull request #4 do
[chungty/unjiggle](https://github.com/chungty/unjiggle) descobriu sobre o `setIconState`. As
anotações sobre o formato do estado dos ícones no [facebook/idb](https://github.com/facebook/idb)
também ajudaram. Nenhum código foi copiado de nenhum dos dois projetos.

A comunicação com o aparelho passa pelo [pymobiledevice3](https://github.com/doronz88/pymobiledevice3),
incluindo o suporte a RemotePairing e o túnel em espaço de usuário para o Wi-Fi, e o acesso USB
pelo [usbmuxd](https://github.com/libimobiledevice/usbmuxd), do projeto libimobiledevice. O
editor no navegador é feito com [Preact](https://preactjs.com) e [htm](https://github.com/developit/htm)
e servido por [Starlette](https://www.starlette.io) e [uvicorn](https://www.uvicorn.org).

## Licença

[MIT](LICENSE). O IconShuffle depende do pymobiledevice3, licenciado sob GPL-3.0-or-later; se
você distribuir os dois juntos como um único programa, essa combinação fica sob a GPL. O editor
no navegador inclui cópias não modificadas do Preact (MIT), do htm (Apache-2.0) e da fonte IBM
Plex Sans (SIL Open Font License 1.1); as licenças estão ao lado deles em
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) e
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts).
