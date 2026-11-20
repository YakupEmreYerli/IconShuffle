<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <b>简体中文</b></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="IconShuffle 标志：一块紫色玻璃方块从槽位中升起">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>在电脑上整理你的 iPhone 主屏幕。</b><br>
在手机的实时镜像上拖动真实图标，或者直接告诉 AI 智能体你想要什么。<br>
Windows、macOS 和 Linux · USB 或 Wi-Fi · 不需要 Mac，不用越狱，无需账户。
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD-Windows-8b6cff?logo=windows&logoColor=white" alt="下载 Windows 版"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD-macOS-8b6cff?logo=apple&logoColor=white" alt="下载 macOS 版"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD-Linux-8b6cff?logo=linux&logoColor=white" alt="下载 Linux 版"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/%E8%AE%B8%E5%8F%AF%E8%AF%81-MIT-blue" alt="MIT 许可证"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/%E7%BD%91%E7%AB%99-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">官网</a> · <a href="docs/agent-guide.md">智能体指南</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="IconShuffle 演示：编辑器映出一部演示用 iPhone；点“按 A–Z 排序”后图标重新排列，改动列表逐条出现，在按下“应用”之前不会写入任何内容">
</picture>

在六英寸的屏幕上把六十个图标一个个拖到位，它们还一边抖动一边把彼此挤到下一页，这种事谁都不想干。IconShuffle 把你的主屏幕连同真实的图标、文件夹和小组件一起搬到电脑的大屏幕上，让你在那里整理。按下“应用”之前，什么都不会发到手机上；每次写入都会先备份，写完再读回核对，如果手机上的结果对不上，就会自动撤销。

## 安装

**Windows**（PowerShell）：

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS 和 Linux：**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

脚本会从本仓库下载最新版本并完成安装；如果愿意，可以先看看脚本内容：[`install.ps1`](install.ps1)、[`install.sh`](install.sh)。也可以自己到[版本发布页面](https://github.com/YakupEmreYerli/IconShuffle/releases/latest)下载安装包：`IconShuffle-*-windows-x64-setup.exe`、`IconShuffle-*-macos-arm64.dmg` 或 `IconShuffle-*-linux-x86_64.AppImage`。

更喜欢终端？命令行工具是一个 Python 包：

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# 或者
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

安装包暂时还没有签名，所以第一次打开时需要多点一下。macOS 上：系统设置 → 隐私与安全性 → **仍要打开**。Windows 上，SmartScreen 可能会询问一次：**更多信息 → 仍要运行**。

## 三种用法

**应用程序。** 打开 IconShuffle，连接 iPhone。你会看到自己的主屏幕，图标和墙纸都和手机上一样。可以把 App 拖到其他页面或程序坞，把一个 App 拖到另一个 App 上建立文件夹，从 App资源库里拖出 App，或者点 **按 A–Z 排序**。右侧会用简单明了的话列出每一项改动；点 **应用** 就会写入。

**你的 AI 智能体。** Claude Code、Codex、Cursor 或任何编程智能体都能替你完成全部工作。把下面这段粘贴过去，在末尾写上你自己的要求：

```text
请阅读 https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md，
用 ios-homescreen 帮我整理 iPhone 主屏幕。需要的话先安装；在向手机写入任何内容之前，
把每一项改动都列给我看，等我同意。我想要的是：把工作类 App 放进一个文件夹，把游戏移到第 2 页。
```

[智能体指南](docs/agent-guide.md)告诉智能体如何安装和使用这个工具，并要求它必须先把改动给你看、等你同意。连接手机和点“信任”仍然要你亲自来。Claude Code 还有一个流程相同的 skill：把 [`skills/ios-homescreen`](skills/ios-homescreen) 复制到 `~/.claude` 里的 `skills` 文件夹（或项目 `.claude` 文件夹里的 `skills` 文件夹）。

Claude Desktop、Claude Code、Codex、Cursor、VS Code 等 MCP 客户端也可以把 IconShuffle 当作**MCP 服务器**使用，它已内置在桌面应用（无需 Python）和命令行工具中：[设置方法](docs/mcp.md)（英文），也可以在没有手机的演示模式下试用。

**终端。** 你的布局就是一个普通的 TOML 文件。读取下来，用任意编辑器修改，再写回去：

```bash
ios-homescreen pull        # 把手机上的布局读入 layout.toml（只读）
ios-homescreen check       # 查看会有哪些改动（离线）
ios-homescreen push        # 询问、备份、写入、校验，必要时回滚
```

## 安全是设计的出发点

主屏幕协议没有公开文档，而且容不得出错，所以 IconShuffle 从不相信它看不到结果的写入：

- **先备份。** 每次写入在动手之前，都会先保存手机当前的布局。
- **每次都读回核对。** 写入后会重新读取手机，逐个图标与计划比对。
- **自动回滚。** 如果手机上的结果与计划不符，会自动恢复备份。之后也可以用 `ios-homescreen restore latest` 撤销任何一次写入。
- **写入前先询问。** 无论用的是应用程序、终端还是智能体，你都会看到完整的改动列表，由你点头同意。
- **数据留在你的电脑上。** 编辑器只监听 127.0.0.1；布局、图标和备份都不会离开你的电脑。无需账户，没有遥测。

详情见[安全模型的工作原理](docs/reference.md#how-the-safety-model-works)。

## 支持的平台

| | 需要准备什么 | 状态 |
| --- | --- | --- |
| **Windows 10 和 11**（64 位） | Microsoft Store 上的 [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k)（或 iTunes）：它会带来 USB 驱动 | 测试版 |
| **macOS**（Apple 芯片） | 无需额外安装 | 测试版 |
| **Linux** | 已安装并正在运行的 `usbmuxd`（`sudo apt install usbmuxd`、`sudo dnf install usbmuxd`、`sudo pacman -S usbmuxd`） | 稳定版 |

各个系统上的引擎都一样，测试也在三个系统上运行。Windows 和 macOS 之所以标为测试版，是因为还没有在很多真实的 iPhone 上用过：如果你在这两个系统上试用了 IconShuffle，提一个 [issue](https://github.com/YakupEmreYerli/IconShuffle/issues) 告诉我们能用（或不能用），会很有帮助。[docs/platforms.md](docs/platforms.md) 列出了每个系统上自动测试的内容。

所有系统都需要：一部信任这台电脑的 iPhone（用数据线连接一次，解锁手机，点 **信任此电脑** 并输入密码）。完成一次 USB 设置后，iOS 17 及以上版本就可以通过 Wi-Fi 使用。不需要 root，也不需要开发者模式。

## 文档

- [参考手册](docs/reference.md)：所有命令和选项、布局文件、编辑器、[安全模型的工作原理](docs/reference.md#how-the-safety-model-works)、Wi-Fi、文件、Python API、限制和故障排除。
- [智能体指南](docs/agent-guide.md)：AI 智能体安全使用 IconShuffle 需要知道的一切。
- [平台](docs/platforms.md)：每个系统上测试了什么，以及如何作为测试人员提供帮助。

## 参与贡献与安全

开发环境搭建、测试以及设计背后的各种坑，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按照 [SECURITY.md](SECURITY.md) 中的说明私下报告。

## 致谢

带有 `ignored` 列表的字典载荷，来自 [chungty/unjiggle](https://github.com/chungty/unjiggle) 第 4 号拉取请求对 `setIconState` 的发现。[facebook/idb](https://github.com/facebook/idb) 中关于图标状态格式的笔记也提供了帮助。没有从这两个项目复制任何代码。

与设备的通信通过 [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) 完成，包括它的 RemotePairing 支持和用于 Wi-Fi 的用户态隧道；USB 访问则通过 libimobiledevice 项目的 [usbmuxd](https://github.com/libimobiledevice/usbmuxd)。浏览器编辑器使用 [Preact](https://preactjs.com) 和 [htm](https://github.com/developit/htm) 构建，由 [Starlette](https://www.starlette.io) 和 [uvicorn](https://www.uvicorn.org) 提供服务。

## 许可证

[MIT](LICENSE)。IconShuffle 依赖 pymobiledevice3，后者采用 GPL-3.0-or-later 许可证；如果你把两者合在一起作为一个程序分发，这个组合就受 GPL 约束。浏览器编辑器附带了 Preact（MIT）、htm（Apache-2.0）和 IBM Plex Sans 字体（SIL Open Font License 1.1）的未修改副本；它们的许可证就放在旁边，位于 [`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) 和 [`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts)。
