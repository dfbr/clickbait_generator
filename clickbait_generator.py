#!/usr/bin/env python3
"""
Clickbait Story Generator
Uses an LLM to invent a clickbait headline and write the full story, summary,
categories and illustration brief in a single request, then generates the
illustration from that brief and saves everything as a Jekyll post.
"""

import argparse
import base64
import glob
import json
import os
import random
import re
from datetime import datetime


SYSTEM_PROMPT = (
    "You are a creative and positive news reporter in the tabloid tradition "
    "writing clickbait stories."
)

# How many recent headlines to show the model so it avoids repeating itself.
RECENT_HEADLINE_COUNT = 20


def story_schema(category_names: list) -> dict:
    """JSON schema for the single story-generation response (OpenAI structured outputs)."""
    return {
        "name": "clickbait_story",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "headline": {"type": "string"},
                "summary": {"type": "string"},
                "categories": {
                    "type": "array",
                    "items": {"type": "string", "enum": category_names},
                },
                "story": {"type": "string"},
                "image_prompt": {"type": "string"},
                "image_alt": {"type": "string"},
            },
            "required": ["headline", "summary", "categories", "story", "image_prompt", "image_alt"],
            "additionalProperties": False,
        },
    }


def recent_headlines(posts_dir: str = '_posts', limit: int = RECENT_HEADLINE_COUNT) -> list:
    """Return the titles of the most recent posts, newest first."""
    titles = []
    for path in sorted(glob.glob(os.path.join(posts_dir, '*.md')), reverse=True)[:limit]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^title:\s*(.+?)\s*$', line)
                    if m:
                        title = m.group(1)
                        if len(title) >= 2 and title[0] == title[-1] and title[0] in '"\'':
                            title = title[1:-1]
                        titles.append(title)
                        break
        except OSError:
            continue
    return titles


def generate_story(api_key: str, model: str, prompt: str, author: dict,
                   category_names: list, recent: list) -> dict:
    """Make the single LLM call that creates the headline, story, summary,
    categories and image brief. Returns the parsed JSON as a dict."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The openai package is required. Install it with 'pip install openai'.")
    client = OpenAI(api_key=api_key)

    # Static instructions first, per-run details last, so the shared prefix is cacheable.
    user_content = (
        prompt
        + "\n\nAllowed categories: " + json.dumps(category_names)
        + "\n\nAuthor (write in their voice and tone):\n"
        + f"author_name: {author.get('name', '')}\n"
        + f"author_bio: {author.get('bio', '')}\n"
        + "\nRecent headlines on the site (do not repeat or imitate these):\n"
        + "\n".join(f"- {h}" for h in recent)
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_schema", "json_schema": story_schema(category_names)},
        max_completion_tokens=2500,
        reasoning_effort="none",
    )
    message = response.choices[0].message
    if getattr(message, 'refusal', None):
        raise RuntimeError(f"Model refused to write a story: {message.refusal}")
    if response.choices[0].finish_reason == 'length':
        raise RuntimeError("Model response was truncated (hit max_completion_tokens).")

    data = json.loads(message.content)
    for key in ("headline", "story", "summary", "image_prompt"):
        if not str(data.get(key, '')).strip():
            raise RuntimeError(f"Model response is missing '{key}'.")
    return data


def generate_image(api_key: str, image_prompt: str, post_slug: str) -> tuple:
    """Generate an image from the LLM-written prompt with gpt-image-1-mini and save it locally.
    Returns tuple of (full_image_path, preview_image_path)."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The openai package is required. Install it with 'pip install openai'.")

    from PIL import Image
    from io import BytesIO

    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=image_prompt,
        size="1024x1024",
        quality="low",
        n=1,
    )

    # GPT image models always return base64-encoded images
    image_bytes = base64.b64decode(response.data[0].b64_json)

    images_dir = 'assets/images'
    os.makedirs(images_dir, exist_ok=True)
    image_filename = f"{images_dir}/{post_slug}.png"
    preview_filename = f"{images_dir}/{post_slug}-preview.png"

    with open(image_filename, 'wb') as f:
        f.write(image_bytes)

    # Create preview (300x300)
    img = Image.open(BytesIO(image_bytes))
    img.thumbnail((300, 300), Image.Resampling.LANCZOS)
    img.save(preview_filename, 'PNG')

    return image_filename, preview_filename


def slugify(value):
    """Convert a string to a URL-friendly slug."""
    value = value.lower()
    value = re.sub(r'[^a-z0-9\s-]', '', value)
    value = re.sub(r'\s+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')


def yaml_str(value: str) -> str:
    """Quote a string for YAML front matter (JSON strings are valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Create a complete clickbait story (headline, text and image) with OpenAI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --openai_key sk-...
  %(prog)s --no-images
        """
    )
    parser.add_argument('--openai_key', required=False, help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('--model', default='gpt-6-luna', help='OpenAI model to use (default: gpt-6-luna)')
    parser.add_argument('--prompt', default='story_prompt.txt', help='Story prompt file (default: story_prompt.txt)')
    parser.add_argument('--no-images', action='store_true', help='Skip image generation and use placeholders')
    args = parser.parse_args()

    if not args.openai_key:
        args.openai_key = os.environ.get('OPENAI_API_KEY')
    if not args.openai_key:
        parser.error('OpenAI API key is required. Provide --openai_key or set OPENAI_API_KEY environment variable.')

    try:
        with open(args.prompt, 'r', encoding='utf-8') as f:
            story_prompt = f.read().strip()

        # Authors: canonical source of truth is _data/authors.json
        authors_file = os.path.join('_data', 'authors.json')
        if not os.path.exists(authors_file):
            raise RuntimeError('No authors available: _data/authors.json not found. Please create it.')
        try:
            with open(authors_file, 'r', encoding='utf-8') as af:
                authors = json.load(af)
        except Exception as e:
            raise RuntimeError(f"Failed to load authors from {authors_file}: {e}")

        author = random.choice(authors)
        # Relative path; Jekyll's `relative_url` filter applies site.baseurl when rendering.
        author_link = f"about.html#{author['id']}"

        categories_file = os.path.join('_data', 'categories.json')
        categories = []
        if os.path.exists(categories_file):
            try:
                with open(categories_file, 'r', encoding='utf-8') as cf:
                    categories = json.load(cf)
            except Exception as e:
                print(f"Warning: failed to load categories: {e}")
        if not categories:
            categories = [
                {"id": "news", "name": "News"},
                {"id": "science", "name": "Science"},
                {"id": "culture", "name": "Culture"},
                {"id": "opinion", "name": "Opinion"}
            ]
        category_names = [c['name'] if isinstance(c, dict) else str(c) for c in categories]

        # The one LLM call: headline, story, summary, categories and image brief
        print(f"Generating story with {args.model}...")
        story = generate_story(
            args.openai_key, args.model, story_prompt, author,
            category_names, recent_headlines(),
        )

        post_title = story['headline'].strip()
        print(f"Headline: {post_title}")
        post_slug = slugify(post_title)
        now = datetime.now()
        post_date = now.strftime('%Y-%m-%d')
        post_datetime = now.strftime('%Y-%m-%d %H:%M:%S +0000')

        if args.no_images:
            print("Skipping image generation (--no-images); using placeholder paths")
            print(f"Image prompt would have been: {story['image_prompt']}")
            image_url = "/assets/images/placeholder.png"
            preview_url = "/assets/images/placeholder-preview.png"
        else:
            print("Generating image with gpt-image-1-mini...")
            image_path, preview_path = generate_image(args.openai_key, story['image_prompt'], post_slug)
            image_url = f"/assets/images/{post_slug}.png"
            preview_url = f"/assets/images/{post_slug}-preview.png"
            print(f"Image saved to {image_path}")
            print(f"Preview saved to {preview_path}")

        # Categories chosen by the model (schema restricts them to the allowed names)
        chosen_cat_names = []
        for name in story.get('categories', []):
            if name in category_names and name not in chosen_cat_names:
                chosen_cat_names.append(name)
        chosen_cat_names = chosen_cat_names[:2] or [category_names[0]]
        categories_field = ['articles'] + chosen_cat_names
        cats_line = "[" + ", ".join(yaml_str(c) for c in categories_field) + "]"

        is_featured = random.random() < 0.2  # occasionally mark a story as featured

        fm_lines = [
            "---",
            "layout: post",
            f"title: {yaml_str(post_title)}",
            f"date: {post_datetime}",
            f"categories: {cats_line}",
            f"category: {yaml_str(chosen_cat_names[0])}",
        ]
        if is_featured:
            fm_lines.append("featured: true")
        fm_lines += [
            f"image: {image_url}",
            f"preview_image: {preview_url}",
        ]
        image_alt = str(story.get('image_alt', '')).strip()
        if image_alt:
            fm_lines.append(f"image_alt: {yaml_str(image_alt)}")
        fm_lines += [
            f"summary: {yaml_str(story['summary'].strip())}",
            f"author: {yaml_str(author['name'])}",
            f"author_id: {yaml_str(author['id'])}",
            f"author_url: {yaml_str(author_link)}",
            "---",
            "",
            "![{{ page.image_alt | default: page.title }}]({{ page.image | relative_url }})",
            "",
        ]
        front_matter = "\n".join(fm_lines)

        # Safeguard: drop any byline the model added despite instructions
        lines = story['story'].strip().splitlines()
        if lines and re.match(r"^By \[.+\]\(.+\)\s*$", lines[0].strip()):
            lines = lines[1:]
            while lines and lines[0].strip() == '':
                lines = lines[1:]
        story_text = '\n'.join(lines) + '\n'

        # Canonical byline using Jekyll relative_url so baseurl is respected
        byline = f"By [{author.get('name')}]({{{{ '{author_link}' | relative_url }}}})\n\n"

        post_dir = '_posts'
        os.makedirs(post_dir, exist_ok=True)
        post_filename = f"{post_dir}/{post_date}-{post_slug}.md"
        with open(post_filename, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(byline)
            f.write(story_text)

        print(f"Story saved to {post_filename}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
