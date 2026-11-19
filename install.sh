#!/bin/sh
# Installs the IconShuffle desktop app on macOS or Linux:
#
#   curl -fsSL https://iconshuffle.app/install.sh | sh
#
# It downloads the latest release from GitHub and installs it:
#   macOS  IconShuffle.app in /Applications (~/Applications without write access there)
#   Linux  the AppImage as ~/.local/bin/iconshuffle, with a menu entry and icon
#
# Settings (environment variables):
#   ICONSHUFFLE_VERSION  a release such as 0.2.0 instead of the latest
#   ICONSHUFFLE_REPO     the GitHub repository (default YakupEmreYerli/IconShuffle)
set -eu

repo="${ICONSHUFFLE_REPO:-YakupEmreYerli/IconShuffle}"
version="${ICONSHUFFLE_VERSION:-}"
releases="https://github.com/$repo/releases"

say() { printf '%s\n' "$*"; }
fail() { printf 'IconShuffle installer: %s\n' "$*" >&2; exit 1; }
command -v curl >/dev/null 2>&1 || fail "curl is needed"

system="$(uname -s)"
arch="$(uname -m)"
case "$system" in
  Darwin)
    # A shell under Rosetta reports x86_64 on Apple silicon.
    [ "$(sysctl -n hw.optional.arm64 2>/dev/null || echo 0)" = 1 ] && arch=arm64
    [ "$arch" = arm64 ] || fail "IconShuffle needs a Mac with Apple silicon (M1 or later)."
    asset=macos-arm64.dmg ;;
  Linux)
    [ "$arch" = x86_64 ] || fail "there is no build for $arch Linux yet; see $releases"
    asset=linux-x86_64.AppImage ;;
  *)
    fail "this script is for macOS and Linux. On Windows run in PowerShell:
  irm https://iconshuffle.app/install.ps1 | iex" ;;
esac

if [ -z "$version" ]; then
  # github.com/OWNER/REPO/releases/latest redirects to .../releases/tag/vX.Y.Z
  latest="$(curl -fsSLI -o /dev/null -w '%{url_effective}' "$releases/latest")" ||
    fail "cannot reach $releases"
  case "$latest" in */releases/tag/*) ;; *) fail "$repo has no release yet" ;; esac
  version="${latest##*/}"
fi
version="${version#v}"
file="IconShuffle-$version-$asset"

tmp="$(mktemp -d)"
mnt=""
cleanup() {
  [ -z "$mnt" ] || hdiutil detach -quiet "$mnt" 2>/dev/null || true
  rm -rf "$tmp"
}
trap cleanup EXIT
trap 'exit 1' INT TERM

say "Downloading $file..."
curl -fL --progress-bar -o "$tmp/$file" "$releases/download/v$version/$file" ||
  fail "download failed: $releases/download/v$version/$file"

if [ "$system" = Darwin ]; then
  mnt="$tmp/mount"
  mkdir "$mnt"
  hdiutil attach -quiet -nobrowse -readonly -mountpoint "$mnt" "$tmp/$file"
  dest=/Applications
  [ -w "$dest" ] || { dest="$HOME/Applications"; mkdir -p "$dest"; }
  rm -rf "$dest/IconShuffle.app"
  cp -R "$mnt/IconShuffle.app" "$dest/"
  # The app is not signed by Apple yet; without this macOS refuses to open a download.
  xattr -dr com.apple.quarantine "$dest/IconShuffle.app" 2>/dev/null || true
  say "Installed $dest/IconShuffle.app ($version)."
  say "(The app is not signed by Apple yet, so the download mark that would block it was removed.)"
  say "Open it from Launchpad or with: open \"$dest/IconShuffle.app\""
  exit 0
fi

bin="$HOME/.local/bin"
share="${XDG_DATA_HOME:-$HOME/.local/share}"
mkdir -p "$bin" "$share/applications" "$share/icons/hicolor/512x512/apps"
mv "$tmp/$file" "$bin/iconshuffle"
chmod +x "$bin/iconshuffle"
# The icon is inside the AppImage; extracting one file needs no FUSE.
if (cd "$tmp" && "$bin/iconshuffle" --appimage-extract iconshuffle.png >/dev/null 2>&1); then
  cp "$tmp/squashfs-root/iconshuffle.png" "$share/icons/hicolor/512x512/apps/iconshuffle.png"
fi
cat > "$share/applications/iconshuffle.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=IconShuffle
Comment=Arrange your iPhone Home Screen
Exec=$bin/iconshuffle
Icon=iconshuffle
Categories=Utility;
EOF
say "Installed $bin/iconshuffle ($version), with a menu entry."
case ":$PATH:" in *":$bin:"*) ;; *) say "Add $bin to your PATH to start it with: iconshuffle" ;; esac
if ! command -v usbmuxd >/dev/null 2>&1; then
  say "For the USB cable, install usbmuxd (e.g. sudo apt install usbmuxd)."
fi
if ! { ldconfig -p 2>/dev/null | grep -q 'libfuse\.so\.2'; }; then
  say "AppImages need libfuse2 (sudo apt install libfuse2t64, or libfuse2 on older systems)."
fi
