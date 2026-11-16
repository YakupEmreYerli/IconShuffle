"""Make build/icons/iconshuffle.{ico,icns,png} from docs/assets/logo.png (needs Pillow)."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
out = ROOT / "build" / "icons"
out.mkdir(parents=True, exist_ok=True)
# The logo is already a rounded tile on the brand's dark ground.
icon = Image.open(ROOT / "docs" / "assets" / "logo.png").convert("RGBA")
icon.save(out / "iconshuffle.png")
icon.save(out / "iconshuffle.ico", sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
icon.save(out / "iconshuffle.icns")
print(f"icons in {out}")
