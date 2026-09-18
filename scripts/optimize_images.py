"""Generate display derivatives; original images remain the lightbox sources.
Run with Python 3 and Pillow 11.3.0: python3 scripts/optimize_images.py
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'images'
THUMBNAILS = ('dokutu', 'taiken', 'hoshi', 'kaya2', 'ana', 'raku', 'chie',
              'kawa', 'mushi', 'gyara', 'kotatu', 'hotaru', 'BBQ1',
              'akuse1', 'akuse2', 'p', 'stamp1', 'stamp2')


def save(source, name, size=None, square=False, lossless=False, quality=88):
    with Image.open(ROOT / source) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        if square:
            image = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)
        elif size:
            image.thumbnail(size, Image.Resampling.LANCZOS)
        output = OUT / name
        image.save(output, 'WEBP', quality=quality, method=6, lossless=lossless)
        print(f'{source}: {(ROOT / source).stat().st_size} -> {name}: {output.stat().st_size} bytes ({image.width}x{image.height})')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep full dimensions and existing cover positioning for large photos.
    for stem in ('top', '120', 'shizen', 'kominka'):
        save(f'{stem}.jpg', f'{stem}.webp')
    # CHARM cards use background-size: cover in an aspect-ratio 4/3 box, so a
    # landscape photo fills the box by height: needed pixels = box height x DPR,
    # not box width. On iPhones (<=430 CSS px) the card is at most 292.5 CSS px
    # tall, i.e. 878 device px at DPR3, so cap taiken.jpg (1567x1045) at 880px tall.
    # 120.jpg (1400x788) is already below that and must stay at full size.
    save('taiken.jpg', 'taiken.webp', (10000, 880))
    # Same 3:1 aspect ratio; use the original logo for larger/DPR-heavy screens.
    for width in (342, 780):
        save('moji.jpg', f'moji-{width}.webp', (width, width // 3), lossless=True)
    # Covers 2x of the 680px hero cap (1360px) and keeps the exact 3:1 ratio.
    # Lossless would be 171KB here (larger than the source JPEG), so this one is
    # lossy; against the lossless version at display size the largest per-channel
    # difference is 6/255.
    save('moji.jpg', 'moji-1362.webp', (1362, 454), quality=90)
    # Existing center/cover thumbnails: 3x density for 72px and 80px slots.
    for stem in THUMBNAILS:
        size = 240 if stem.startswith('stamp') else 216
        save(f'{stem}.jpg', f'{stem}-thumb.webp', size, square=True)
