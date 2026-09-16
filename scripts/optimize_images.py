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


def save(source, name, size=None, square=False, lossless=False):
    with Image.open(ROOT / source) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        if square:
            image = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)
        elif size:
            image.thumbnail(size, Image.Resampling.LANCZOS)
        output = OUT / name
        image.save(output, 'WEBP', quality=88, method=6, lossless=lossless)
        print(f'{source}: {(ROOT / source).stat().st_size} -> {name}: {output.stat().st_size} bytes ({image.width}x{image.height})')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep full dimensions and existing cover positioning for large photos.
    for stem in ('top', '120', 'taiken', 'shizen', 'kominka'):
        save(f'{stem}.jpg', f'{stem}.webp')
    # Same 3:1 aspect ratio; use the original logo for larger/DPR-heavy screens.
    for width in (342, 780):
        save('moji.jpg', f'moji-{width}.webp', (width, width // 3), lossless=True)
    # Existing center/cover thumbnails: 3x density for 72px and 80px slots.
    for stem in THUMBNAILS:
        size = 240 if stem.startswith('stamp') else 216
        save(f'{stem}.jpg', f'{stem}-thumb.webp', size, square=True)
