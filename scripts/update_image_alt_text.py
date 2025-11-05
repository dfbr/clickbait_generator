#!/usr/bin/env python3
"""
Update all post files to use dynamic image alt text.
Changes ![Title](url) to ![{{ page.image_alt | default: page.title }}](url)
"""

import os
import re

def update_post_alt_text(filepath):
    """Update image alt text in a post file to use Liquid variable."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match image markdown: ![any text]({{ any url }})
    # We want to replace both the alt text AND ensure the URL uses page.image
    pattern = r'!\[([^\]]+)\]\(\{\{\s*([^}]+)\s*\}\}\)'
    
    def replacer(match):
        url_part = match.group(2).strip()
        # If the URL is already using page.image, keep it; otherwise update it
        if 'page.image' in url_part:
            return f'![{{{{ page.image_alt | default: page.title }}}}]({{{{ {url_part} }}}})'
        else:
            # Replace hardcoded path with page.image
            return '![{{ page.image_alt | default: page.title }}]({{ page.image | relative_url }})'
    
    updated_content = re.sub(pattern, replacer, content)
    
    if updated_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

def main():
    posts_dir = '_posts'
    updated_count = 0
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            if update_post_alt_text(filepath):
                print(f"Updated: {filename}")
                updated_count += 1
    
    print(f"\nDone! Updated {updated_count} files.")

if __name__ == '__main__':
    main()
