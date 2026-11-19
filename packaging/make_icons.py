"""Make build/icons/iconshuffle.{ico,icns,png} from docs/assets/logo.png (needs Pillow)."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"
out = ROOT / "build" / "icons"
out.mkdir(parents=True, exist_ok=True)
# The glass logo blurs below 48 px, so 16 and 32 px come from the simplified drawing
# (logo-small.svg rendered to logo-16.png and logo-32.png).
icon = Image.open(ASSETS / "logo.png").convert("RGBA")
small = [Image.open(ASSETS / f"logo-{s}.png").convert("RGBA") for s in (16, 32)]
icon.save(out / "iconshuffle.png")
icon.save(
    out / "iconshuffle.ico",
    sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)],
    append_images=small,
)
icon.save(out / "iconshuffle.icns")
print(f"icons in {out}")
