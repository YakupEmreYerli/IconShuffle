<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <b>Français</b> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="Logo d'IconShuffle : une tuile de verre violette qui se soulève de son emplacement">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>Réorganisez l'écran d'accueil de votre iPhone depuis votre ordinateur.</b><br>
Déplacez vos vraies icônes sur un miroir en direct de votre téléphone, ou dites simplement à votre agent IA ce que vous voulez.<br>
Windows, macOS et Linux · USB ou Wi-Fi · sans Mac, sans jailbreak, sans compte.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/T%C3%A9l%C3%A9charger-Windows-8b6cff?logo=windows&logoColor=white" alt="Télécharger pour Windows"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/T%C3%A9l%C3%A9charger-macOS-8b6cff?logo=apple&logoColor=white" alt="Télécharger pour macOS"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/T%C3%A9l%C3%A9charger-Linux-8b6cff?logo=linux&logoColor=white" alt="Télécharger pour Linux"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-blue" alt="Licence MIT"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Site web</a> · <a href="docs/agent-guide.md">Guide pour agents</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="Démo d'IconShuffle : l'éditeur reflète un iPhone de démonstration ; Trier de A à Z réorganise les icônes, la liste des modifications se remplit, et rien n'est écrit avant d'appuyer sur Appliquer">
</picture>

Trier soixante icônes en les faisant glisser une à une sur un écran de six pouces, pendant
qu'elles tremblent et se poussent sur la page suivante, n'amuse personne. IconShuffle affiche
votre écran d'accueil sur le grand écran de votre ordinateur, avec vos vraies icônes, vos
dossiers et vos widgets, et vous laisse l'organiser là. Rien n'arrive sur le téléphone avant
que vous appuyiez sur Appliquer, et chaque écriture est sauvegardée, relue, puis annulée
d'elle-même si le téléphone ne correspond pas.

## Installation

**Windows** (PowerShell) :

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS et Linux :**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

Les scripts téléchargent la dernière version publiée dans ce dépôt et l'installent ; lisez-les
d'abord si vous le souhaitez : [`install.ps1`](install.ps1), [`install.sh`](install.sh). Vous
pouvez aussi récupérer l'installateur vous-même sur la [page des versions](https://github.com/YakupEmreYerli/IconShuffle/releases/latest) :
`IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg` ou
`IconShuffle-*-linux-x86_64.AppImage`.

Vous préférez le terminal ? L'outil en ligne de commande est un paquet Python :

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# ou
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

Les builds ne sont pas encore signés, le premier lancement demande donc un clic de plus. Sur
macOS : Réglages Système → Confidentialité et sécurité → **Ouvrir quand même**. Sur Windows,
SmartScreen peut vous avertir une fois : **Informations complémentaires → Exécuter quand même**.

## Trois façons de l'utiliser

**L'application.** Ouvrez IconShuffle et branchez votre iPhone. Vous voyez votre écran
d'accueil avec ses propres icônes et son fond d'écran. Faites glisser des apps d'une page à
l'autre et dans le Dock, déposez une app sur une autre pour créer un dossier, sortez des apps
de la Bibliothèque d'apps ou appuyez sur **Trier de A à Z**. La partie droite liste chaque
modification en termes simples ; **Appliquer** les écrit.

**Votre agent IA.** Claude Code, Codex, Cursor ou n'importe quel agent de programmation peut
tout faire à votre place. Collez ceci, avec votre propre souhait à la fin :

```text
Lis https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md et
aide-moi à réorganiser l'écran d'accueil de mon iPhone avec ios-homescreen. Installe-le si
nécessaire, montre-moi chaque modification avant que quoi que ce soit soit écrit sur le
téléphone, et attends mon accord. Ce que je veux : mets mes apps de travail dans un seul
dossier et déplace les jeux en page 2.
```

Le [guide pour agents](docs/agent-guide.md) explique à l'agent comment installer et piloter
l'outil, et lui indique qu'il doit vous montrer les modifications et attendre votre accord.
C'est toujours vous qui branchez le téléphone et touchez Se fier. Pour Claude Code, il existe
aussi un skill qui suit le même déroulement : copiez [`skills/ios-homescreen`](skills/ios-homescreen)
dans le dossier `skills` de `~/.claude` (ou du dossier `.claude` d'un projet).

Claude Desktop, Claude Code, Codex, Cursor, VS Code et les autres clients MCP peuvent
aussi utiliser IconShuffle comme **serveur MCP**, intégré à l'application de bureau
(sans Python) et à l'outil en ligne de commande : [le configurer](docs/mcp.md) (en
anglais), ou l'essayer sans téléphone en mode démo.

**Le terminal.** Votre disposition est un simple fichier TOML. Récupérez-la, modifiez-la dans
n'importe quel éditeur, renvoyez-la :

```bash
ios-homescreen pull        # lit le téléphone dans layout.toml (lecture seule)
ios-homescreen check       # montre ce qui changerait (hors connexion)
ios-homescreen push        # demande, sauvegarde, écrit, vérifie, annule si besoin
```

## Sûr par conception

Le protocole de l'écran d'accueil n'est pas documenté et ne pardonne rien, alors IconShuffle
ne fait jamais confiance à une écriture qu'il ne peut pas vérifier :

- **D'abord une sauvegarde.** Chaque écriture enregistre la disposition actuelle du téléphone
  avant de toucher à quoi que ce soit.
- **Relu à chaque fois.** Après l'écriture, le téléphone est relu et comparé au plan, icône
  par icône.
- **Revient en arrière tout seul.** Si le téléphone ne correspond pas, la sauvegarde est remise
  en place automatiquement. `ios-homescreen restore latest` annule n'importe quelle écriture,
  même plus tard.
- **Demande avant d'écrire.** Vous voyez la liste complète des modifications et donnez votre
  accord, que vous passiez par l'application, le terminal ou un agent.
- **Reste sur votre ordinateur.** L'éditeur écoute uniquement sur 127.0.0.1 ; dispositions,
  icônes et sauvegardes ne quittent jamais votre machine. Pas de compte, pas de télémétrie.

Les détails sont dans [le fonctionnement du modèle de sécurité](docs/reference.md#how-the-safety-model-works).

## Plateformes

| | Ce qu'il vous faut | État |
| --- | --- | --- |
| **Windows 10 et 11** (64 bits) | [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) depuis le Microsoft Store (ou iTunes) : il apporte le pilote USB | Bêta |
| **macOS** (puce Apple) | Rien de plus | Bêta |
| **Linux** | `usbmuxd`, installé et en cours d'exécution (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Stable |

Le moteur est le même sur chaque système et ses tests tournent sur les trois. Windows et macOS
sont marqués bêta parce qu'ils n'ont pas encore rencontré beaucoup de vrais iPhone : si vous
essayez IconShuffle sur l'un d'eux, une [issue](https://github.com/YakupEmreYerli/IconShuffle/issues)
qui dit que ça a marché (ou pas) aide beaucoup. [docs/platforms.md](docs/platforms.md) liste ce
qui est testé automatiquement sur chaque système.

Sur tous les systèmes : un iPhone qui fait confiance à l'ordinateur (branchez-le une fois avec
un câble, déverrouillez-le, touchez **Se fier à cet ordinateur** et saisissez le code). Le
Wi-Fi fonctionne avec iOS 17 ou ultérieur, après une configuration unique en USB. Pas de root,
pas de mode développeur.

## Documentation

- [Référence](docs/reference.md) : toutes les commandes et options, le fichier de disposition,
  l'éditeur, [le fonctionnement du modèle de sécurité](docs/reference.md#how-the-safety-model-works), le
  Wi-Fi, les fichiers, l'API Python, les limites et le dépannage.
- [Guide pour agents](docs/agent-guide.md) : ce dont un agent IA a besoin pour piloter IconShuffle
  en toute sécurité.
- [Plateformes](docs/platforms.md) : ce qui est testé sur chaque système, et comment aider en
  tant que bêta-testeur.

## Contribuer et sécurité

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour l'installation, les tests et les pièges qui
expliquent la conception. Signalez les problèmes de sécurité en privé, comme décrit dans
[SECURITY.md](SECURITY.md).

## Remerciements

Le payload sous forme de dictionnaire avec une liste `ignored` vient de ce que la pull request
n° 4 de [chungty/unjiggle](https://github.com/chungty/unjiggle) a découvert sur `setIconState`.
Les notes sur le format d'état des icônes dans [facebook/idb](https://github.com/facebook/idb)
ont aussi aidé. Aucun code n'a été copié de ces deux projets.

La communication avec l'appareil passe par [pymobiledevice3](https://github.com/doronz88/pymobiledevice3),
y compris sa prise en charge de RemotePairing et son tunnel en espace utilisateur pour le
Wi-Fi, et l'accès USB par [usbmuxd](https://github.com/libimobiledevice/usbmuxd), issu du
projet libimobiledevice. L'éditeur dans le navigateur est construit avec
[Preact](https://preactjs.com) et [htm](https://github.com/developit/htm), et servi par
[Starlette](https://www.starlette.io) et [uvicorn](https://www.uvicorn.org).

## Licence

[MIT](LICENSE). IconShuffle dépend de pymobiledevice3, distribué sous licence
GPL-3.0-or-later ; si vous distribuez les deux ensemble comme un seul programme, cette
combinaison relève de la GPL. L'éditeur dans le navigateur inclut des copies non modifiées de
Preact (MIT), htm (Apache-2.0) et de la police IBM Plex Sans (SIL Open Font License 1.1) ;
leurs licences se trouvent à côté, dans
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) et
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts).
