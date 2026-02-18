#!/usr/bin/env python3
"""
Scan Images/galleries and generate scripts/all-images.js which defines
window.ALL_GALLERY_IMAGES as an array of image paths (paths are relative
to pages in `gallery pages/`, e.g. "../Images/galleries/...jpg").

Run when you add or remove images so the random viewer stays up to date.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERIES = ROOT / 'Images' / 'galleries'
OUT = ROOT / 'scripts' / 'all-images.js'

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def main():
    images = []
    if not GALLERIES.exists():
        print('Galleries folder not found:', GALLERIES)
        return

    for folder in sorted(GALLERIES.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name.lower() == 'textures':
            continue
        for p in sorted(folder.iterdir()):
            if p.suffix.lower() in ALLOWED_EXT:
                # path relative to gallery pages (which live in gallery pages/)
                rel = f"../Images/galleries/{folder.name}/{p.name}"
                images.append(rel)

    OUT.write_text('window.ALL_GALLERY_IMAGES = [\n' + ',\n'.join(f'  "{i}"' for i in images) + '\n];\n', encoding='utf-8')
    print(f'Wrote {len(images)} images to {OUT}')


if __name__ == '__main__':
    main()
