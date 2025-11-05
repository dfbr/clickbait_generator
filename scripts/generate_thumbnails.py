#!/usr/bin/env python3
"""
Generate 128x128 thumbnail images for author portraits in assets/images/team.
Creates files with the suffix -thumb.png next to the original files.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(__file__))
TEAM_DIR = os.path.join(ROOT, "assets", "images", "team")

THUMB_SIZE = (128, 128)

if not os.path.isdir(TEAM_DIR):
    print("Team images directory not found:", TEAM_DIR)
    raise SystemExit(1)

count = 0
for fname in os.listdir(TEAM_DIR):
    if fname.lower().endswith(('-thumb.png', '-thumb.jpg', '-thumb.jpeg')):
        continue
    if not fname.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    base, ext = os.path.splitext(fname)
    thumb_name = f"{base}-thumb.png"
    thumb_path = os.path.join(TEAM_DIR, thumb_name)
    src_path = os.path.join(TEAM_DIR, fname)
    if os.path.exists(thumb_path):
        print("Skipping existing thumbnail:", thumb_name)
        continue
    try:
        with Image.open(src_path) as im:
            im = im.convert('RGBA')
            im.thumbnail(THUMB_SIZE, Image.LANCZOS)
            # Create a square canvas and paste centered
            canvas = Image.new('RGBA', THUMB_SIZE, (255, 255, 255, 0))
            w, h = im.size
            x = (THUMB_SIZE[0] - w) // 2
            y = (THUMB_SIZE[1] - h) // 2
            canvas.paste(im, (x, y), im)
            # Save as PNG
            canvas.save(thumb_path, format='PNG')
            print(f"Created thumbnail: {thumb_name}")
            count += 1
    except Exception as e:
        print(f"Failed to process {fname}: {e}")

print(f"Done. Created {count} thumbnails.")
