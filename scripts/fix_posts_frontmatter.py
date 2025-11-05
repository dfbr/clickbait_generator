#!/usr/bin/env python3
"""Fix YAML front matter indentation in _posts files.
This script will:
- Find the first YAML front matter block (--- ... ---) and left-strip leading whitespace on each front-matter line so keys start at column 0.
- Remove 8 leading spaces from any line in the file that begins with exactly 8 spaces (this fixes image and byline lines generated earlier).

Run in repo root: python scripts/fix_posts_frontmatter.py
"""
import glob
import io

posts = glob.glob('_posts/*.md')
if not posts:
    print('No posts found in _posts/')
    raise SystemExit(0)

for p in posts:
    with io.open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # find front matter
    try:
        start = next(i for i,l in enumerate(lines) if l.strip() == '---')
        end = next(i for i,l in enumerate(lines[start+1:], start+1) if l.strip() == '---')
    except StopIteration:
        print(f'No front matter found in {p}, skipping')
        continue

    # Strip leading whitespace in front matter lines (start..end)
    for i in range(start+1, end):
        lines[i] = lines[i].lstrip()

    # For rest of file, remove 8 leading spaces where present (fix image/byline lines)
    for i in range(end+1, len(lines)):
        if lines[i].startswith('        '):  # 8 spaces
            lines[i] = lines[i][8:]

    # Ensure the opening and closing --- are at column 0
    lines[start] = '---\n'
    lines[end] = '---\n'

    with io.open(p, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'Fixed {p}')

print('Done')
