#!/usr/bin/env python3
"""
Scans Images/textures/ and writes scripts/bg-list.js containing a JS array
window.BG_TEXTURES = [ ... ];

Run: python3 scripts/generate_bg_list.py
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXTURE_DIR = ROOT / 'Images' / 'textures'
OUT_FILE = ROOT / 'scripts' / 'bg-list.js'

exts = {'.jpg', '.jpeg', '.png', '.gif'}

files = []
if TEXTURE_DIR.exists() and TEXTURE_DIR.is_dir():
    for p in sorted(TEXTURE_DIR.iterdir()):
        if p.suffix.lower() in exts and p.is_file():
            files.append(p.name)

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated list of texture filenames for random backgrounds\n')
    f.write('window.BG_TEXTURES = [\n')
    for i, name in enumerate(files):
        comma = ',' if i < len(files)-1 else ''
        f.write(f'  "{name}"{comma}\n')
    f.write('];\n')

print(f'Wrote {len(files)} textures to {OUT_FILE}')
