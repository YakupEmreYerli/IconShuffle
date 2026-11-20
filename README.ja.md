<p align="center"><a href="README.md">English</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <b>日本語</b> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="IconShuffleのロゴ：スロットから浮き上がるバイオレットのガラスタイル">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>iPhoneのホーム画面をパソコンで並べ替え。</b><br>
iPhoneの画面をそのまま映したエディタで本物のアイコンをドラッグするか、AIエージェントにやりたいことを伝えるだけです。<br>Windows・macOS・Linux · USBまたはWi-Fi · Mac、脱獄、アカウントは不要です。
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89-Windows-8b6cff?logo=windows&logoColor=white" alt="Windows版をダウンロード"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89-macOS-8b6cff?logo=apple&logoColor=white" alt="macOS版をダウンロード"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89-Linux-8b6cff?logo=linux&logoColor=white" alt="Linux版をダウンロード"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9-MIT-blue" alt="MITライセンス"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/%E3%82%B5%E3%82%A4%E3%83%88-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Webサイト</a> · <a href="docs/agent-guide.md">エージェント向けガイド</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="IconShuffleのデモ：エディタがデモ用のiPhoneを映し出し、「名前順に並べる」でアイコンが並べ替わり、変更リストが埋まっていきます。「適用」を押すまでは何も書き込まれません">
</picture>

6インチの画面で60個のアイコンを1つずつドラッグし、そのあいだにアイコンが揺れながら互いを次のページへ押し出していく。そんな作業を楽しいと思う人はいません。IconShuffleは、本物のアイコンやフォルダ、ウィジェットが並んだホーム画面をパソコンの大きな画面に映し出し、そこで並べ替えられるようにします。「適用」を押すまでiPhoneには何も送られません。書き込みのたびにバックアップを取り、iPhoneを読み直して確認し、内容が一致しなければ自動で元に戻します。

## インストール

**Windows**（PowerShell）：

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOSとLinux：**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

スクリプトはこのリポジトリから最新リリースをダウンロードしてインストールします。気になる場合は先に中身を読んでください：[`install.ps1`](install.ps1)、[`install.sh`](install.sh)。[リリースページ](https://github.com/YakupEmreYerli/IconShuffle/releases/latest)からインストーラを直接ダウンロードすることもできます：`IconShuffle-*-windows-x64-setup.exe`、`IconShuffle-*-macos-arm64.dmg`、`IconShuffle-*-linux-x86_64.AppImage`。

ターミナル派の方へ：コマンドラインツールはPythonパッケージとして入手できます。

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# または
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

ビルドにはまだ署名がないため、初回の起動時だけクリックが1回多く必要です。macOSでは、システム設定 → プライバシーとセキュリティ → **このまま開く**。Windowsでは、SmartScreenが一度だけ確認してくることがあります：**詳細情報 → 実行**。

## 3つの使い方

**アプリ。** IconShuffleを開いてiPhoneをつなぎます。ホーム画面が、いつものアイコンと壁紙のまま表示されます。Appをページ間やDockへドラッグしたり、Appを別のAppの上にドロップしてフォルダを作ったり、Appライブラリから引き出したり、**名前順に並べる**を押したりできます。右側にはすべての変更がわかりやすい言葉で一覧表示され、**適用**を押すと書き込まれます。

**AIエージェント。** Claude Code、Codex、Cursorなど、コーディングエージェントならどれでも作業をまるごと任せられます。次の文を貼り付けて、最後に自分の希望を書いてください：

```text
https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md を読んで、
ios-homescreen でiPhoneのホーム画面の並べ替えを手伝ってください。必要ならインストールし、
iPhoneに何か書き込む前にすべての変更を見せて、私のOKを待ってください。やりたいこと：
仕事用のAppを1つのフォルダにまとめて、ゲームを2ページ目に移動する。
```

[エージェント向けガイド](docs/agent-guide.md)には、ツールのインストール方法と使い方、そして変更を必ず見せてあなたのOKを待つことがエージェント向けに書かれています。iPhoneをつないで「信頼」をタップするのは、あなた自身です。Claude Code向けには同じ流れのスキルもあります：[`skills/ios-homescreen`](skills/ios-homescreen)を`~/.claude`内の`skills`フォルダ（またはプロジェクトの`.claude`フォルダ内）にコピーしてください。

Claude Desktop、Claude Code、Codex、Cursor、VS CodeなどのMCPクライアントからは、IconShuffleを**MCPサーバー**として使うこともできます。デスクトップアプリ（Python不要）とコマンドラインツールに組み込まれています：[設定方法](docs/mcp.md)（英語）。iPhoneがなくてもデモモードで試せます。

**ターミナル。** レイアウトはただのTOMLファイルです。読み込んで、好きなエディタで編集し、書き戻します：

```bash
ios-homescreen pull        # iPhoneを読み込んでlayout.tomlに保存（読み取りのみ）
ios-homescreen check       # 何が変わるかを確認（オフライン）
ios-homescreen push        # 確認、バックアップ、書き込み、検証、必要ならロールバック
```

## 安全を最優先した設計

ホーム画面のプロトコルは非公開で、ミスを許してくれません。そのためIconShuffleは、結果を確かめられない書き込みを決して信用しません：

- **まずバックアップ。** 書き込みのたびに、何かに触れる前にiPhoneの現在のレイアウトを保存します。
- **毎回読み直して確認。** 書き込んだあとにiPhoneをもう一度読み込み、アイコン1つずつ計画と照らし合わせます。
- **自動で元に戻す。** iPhoneが計画と一致しなければ、バックアップを自動で書き戻します。`ios-homescreen restore latest`を使えば、あとからどの書き込みでも元に戻せます。
- **書き込む前に確認。** アプリ、ターミナル、エージェントのどれを使っても、変更の一覧をすべて見てからあなたがOKを出します。
- **パソコンの中だけで完結。** エディタは127.0.0.1でのみ待ち受け、レイアウト、アイコン、バックアップがパソコンの外に出ることはありません。アカウントもテレメトリもありません。

詳しくは[安全モデルの仕組み](docs/reference.md#how-the-safety-model-works)をご覧ください。

## 対応プラットフォーム

| | 必要なもの | 状況 |
| --- | --- | --- |
| **Windows 10・11**（64ビット） | Microsoft Storeの[Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k)（またはiTunes）：USBドライバが一緒に入ります | ベータ |
| **macOS**（Appleシリコン） | 追加のものは不要 | ベータ |
| **Linux** | `usbmuxd`をインストールして起動しておくこと（`sudo apt install usbmuxd`、`sudo dnf install usbmuxd`、`sudo pacman -S usbmuxd`） | 安定版 |

エンジンはどのシステムでも同じで、テストは3つすべてで実行しています。WindowsとmacOSをベータとしているのは、まだ実機のiPhoneでの実績が少ないためです。これらのシステムでIconShuffleを試したら、動いた（または動かなかった）ことを[issue](https://github.com/YakupEmreYerli/IconShuffle/issues)で知らせてもらえるととても助かります。各システムで自動テストしている内容は[docs/platforms.md](docs/platforms.md)にまとめています。

どのシステムでも、パソコンを信頼済みのiPhoneが必要です（一度ケーブルでつなぎ、ロックを解除して、「このコンピュータを信頼しますか?」で**信頼**をタップし、パスコードを入力します）。Wi-Fi接続は、USBで一度だけ設定すればiOS 17以降で使えます。rootもデベロッパモードも不要です。

## ドキュメント

- [リファレンス](docs/reference.md)：すべてのコマンドとオプション、レイアウトファイル、エディタ、[安全モデルの仕組み](docs/reference.md#how-the-safety-model-works)、Wi-Fi、ファイル、Python API、制限事項、トラブルシューティング。
- [エージェント向けガイド](docs/agent-guide.md)：AIエージェントがIconShuffleを安全に扱うために必要なこと。
- [プラットフォーム](docs/platforms.md)：各システムでテストしている内容と、ベータテスターとしての協力方法。

## コントリビュートとセキュリティ

セットアップ、テスト、設計の背景にある落とし穴については[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。セキュリティ上の問題は、[SECURITY.md](SECURITY.md)に書かれた方法で非公開で報告してください。

## クレジット

`ignored`リストを含む辞書形式のペイロードは、[chungty/unjiggle](https://github.com/chungty/unjiggle)のプルリクエスト #4 が`setIconState`について明らかにした内容に基づいています。[facebook/idb](https://github.com/facebook/idb)にあるアイコン状態フォーマットのメモも参考になりました。どちらのプロジェクトからもコードはコピーしていません。

デバイスとの通信には[pymobiledevice3](https://github.com/doronz88/pymobiledevice3)（Wi-Fi用のRemotePairingサポートとユーザー空間トンネルを含む）を、USBアクセスにはlibimobiledeviceプロジェクトの[usbmuxd](https://github.com/libimobiledevice/usbmuxd)を使っています。ブラウザ上のエディタは[Preact](https://preactjs.com)と[htm](https://github.com/developit/htm)で作られ、[Starlette](https://www.starlette.io)と[uvicorn](https://www.uvicorn.org)で配信しています。

## ライセンス

[MIT](LICENSE)。IconShuffleはGPL-3.0-or-laterでライセンスされているpymobiledevice3に依存しています。両者を1つのプログラムとしてまとめて配布する場合、その組み合わせはGPLの対象になります。ブラウザ上のエディタには、Preact（MIT）、htm（Apache-2.0）、IBM Plex Sansフォント（SIL Open Font License 1.1）の無改変のコピーが含まれています。それぞれのライセンスは[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor)と[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts)に同梱しています。
