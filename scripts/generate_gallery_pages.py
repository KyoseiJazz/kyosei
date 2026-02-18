#!/usr/bin/env python3
"""
Generate gallery HTML pages from a template for each subfolder in Images/galleries/

Usage: python3 scripts/generate_gallery_pages.py

The script reads `gallery pages/gallery-template.html` and writes
`gallery pages/gallery-<folder>.html` for each folder found in
`Images/galleries/` (excluding `textures`). Existing files are skipped.
"""
from pathlib import Path
from datetime import datetime
import re
import argparse

ROOT = Path(__file__).resolve().parents[1]
GALLERIES_DIR = ROOT / 'Images' / 'galleries'
TEMPLATE_PATH = ROOT / 'gallery pages' / 'gallery-template.html'
OUT_DIR = ROOT / 'gallery pages'

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def slug_to_title(slug: str) -> str:
    return slug.replace('-', ' ').replace('_', ' ').strip().title()


def build_thumbs_markup(folder: Path) -> str:
    files = [p.name for p in sorted(folder.iterdir()) if p.suffix.lower() in ALLOWED_EXT]
    if not files:
        return '                    <!-- no images found -->\n'

    lines = []
    for fn in files:
        caption = Path(fn).stem.replace('-', ' ').replace('_', ' ').strip()
        lines.append(f'                    <a href="../Images/galleries/{folder.name}/{fn}" data-caption="{caption}">')
        lines.append(f'                        <img src="../Images/galleries/{folder.name}/{fn}" alt="{caption}">')
        lines.append('                    </a>')
    return '\n'.join(lines) + '\n'


def generate_page_for_folder(folder_name: str, template: str) -> str:
    title = slug_to_title(folder_name)
    today = datetime.now().strftime('%B %d, %Y')

    # Replace title in <title> tag
    out = re.sub(r'<title>.*?</title>', f'<title>Shunya Carroll - {title}</title>', template, flags=re.S)

    # Replace H2 gallery title
    out = re.sub(r'<h2>.*?</h2>', f'<h2>{title}</h2>', out, count=1, flags=re.S)

    # Replace date placeholder (the specific pattern used in template)
    out = out.replace('<p><strong>Date:</strong> [Insert Date here]</p>', f'<p><strong>Date:</strong> {today}</p>')

    # Replace thumbs block
    thumbs_markup = build_thumbs_markup(GALLERIES_DIR / folder_name)
    out = re.sub(r'(<div class="thumbs">).*?(</div>)', r'\1\n' + thumbs_markup + r'                \2', out, flags=re.S)

    return out


def main():
    parser = argparse.ArgumentParser(description='Generate gallery pages from template')
    parser.add_argument('--force', '-f', action='store_true', help='Overwrite existing gallery pages')
    args = parser.parse_args()

    if not TEMPLATE_PATH.exists():
        print(f"Template not found: {TEMPLATE_PATH}")
        return

    template = TEMPLATE_PATH.read_text(encoding='utf-8')

    created = []
    overwritten = []
    skipped = []

    for p in sorted(GALLERIES_DIR.iterdir()):
        if not p.is_dir():
            continue
        if p.name.lower() == 'textures':
            continue

        out_path = OUT_DIR / f'gallery-{p.name}.html'
        content = generate_page_for_folder(p.name, template)

        if out_path.exists():
            if args.force:
                out_path.write_text(content, encoding='utf-8')
                overwritten.append(out_path)
            else:
                skipped.append(out_path)
            continue

        out_path.write_text(content, encoding='utf-8')
        created.append(out_path)

    if created:
        print(f"Created {len(created)} gallery page(s):")
        for c in created:
            print(f"  - {c}")
    else:
        print("No new gallery pages created.")

    if overwritten:
        print(f"Overwrote {len(overwritten)} page(s):")
        for c in overwritten:
            print(f"  - {c}")

    if skipped:
        print(f"Skipped {len(skipped)} existing page(s):")
        for s in skipped:
            print(f"  - {s}")


if __name__ == '__main__':
    main()
