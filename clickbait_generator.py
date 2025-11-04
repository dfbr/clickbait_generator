#!/usr/bin/env python3
"""
Clickbait Headline Generator
Generates random clickbait headlines using templates and word lists.
"""

import argparse
import random
import json
import os
import re
import requests
from datetime import datetime
from typing import List


class ClickbaitGenerator:
    """Generate clickbait headlines from template patterns."""
    
    def __init__(self, nouns_file: str, adjectives_file: str, verbs_file: str, 
                 celebrities_file: str, professions_file: str, templates_file: str):
        """Initialize the generator with word lists from files."""
        self.nouns = self._load_words(nouns_file)
        self.adjectives = self._load_words(adjectives_file)
        self.verbs = self._load_words(verbs_file)
        self.celebrities = self._load_words(celebrities_file)
        self.professions = self._load_words(professions_file)
        self.templates = self._load_templates(templates_file)
        
        # Common clickbait numbers (weighted towards more clickbait-friendly values)
        self.clickbait_numbers = [3, 5, 7, 10, 12, 15, 17, 20, 25, 30, 50, 100]
    
    def _load_templates(self, filename: str) -> List[str]:
        """Load headline templates from a file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                templates = []
                for line in f:
                    line = line.strip()
                    # Skip comments and blank lines
                    if line and not line.startswith('#'):
                        templates.append(line)
            if not templates:
                raise ValueError(f"No templates found in {filename}")
            return templates
        except FileNotFoundError:
            raise FileNotFoundError(f"Required file not found: {filename}")
        except Exception as e:
            raise Exception(f"Error loading {filename}: {e}")
    
    def _load_words(self, filename: str) -> List[str]:
        """Load words from a file, one word per line."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            if not words:
                raise ValueError(f"File {filename} is empty")
            return words
        except FileNotFoundError:
            raise FileNotFoundError(f"Required file not found: {filename}")
        except Exception as e:
            raise Exception(f"Error loading {filename}: {e}")
    
    def _random_noun(self) -> str:
        """Get a random noun."""
        return random.choice(self.nouns)
    
    def _random_adjective(self) -> str:
        """Get a random adjective."""
        return random.choice(self.adjectives)
    
    def _random_verb(self) -> str:
        """Get a random verb."""
        return random.choice(self.verbs)
    
    def _random_number(self) -> str:
        """Get a random number between 1-100, with preference for clickbait-friendly values."""
        # 70% chance of using clickbait-friendly numbers, 30% chance of random 1-100
        if random.random() < 0.7:
            return str(random.choice(self.clickbait_numbers))
        else:
            return str(random.randint(1, 100))
    
    def _random_percentage(self) -> str:
        """Get a random percentage for 'x% of people' style headlines."""
        # Generate percentage that makes sense (usually low to make it exclusive)
        percentages = [1, 2, 3, 5, 10, 15, 20, 25, 30, 50, 75, 90, 95, 99]
        return str(random.choice(percentages))
    
    def _random_celebrity(self) -> str:
        """Get a random celebrity name."""
        return random.choice(self.celebrities)
    
    def _random_profession(self) -> str:
        """Get a random profession."""
        return random.choice(self.professions)
    
    def _fill_template(self, template: str) -> str:
        """Fill a template string with random values."""
        result = template
        
        # Replace all placeholders - need to handle multiple occurrences
        while '<number>' in result:
            result = result.replace('<number>', self._random_number(), 1)
        
        while '<percentage>' in result:
            result = result.replace('<percentage>', self._random_percentage(), 1)
        
        while '<adjective>' in result:
            result = result.replace('<adjective>', self._random_adjective(), 1)
        
        while '<noun>' in result:
            result = result.replace('<noun>', self._random_noun(), 1)
        
        while '<verb>' in result:
            result = result.replace('<verb>', self._random_verb(), 1)
        
        while '<celebrity>' in result:
            result = result.replace('<celebrity>', self._random_celebrity(), 1)
        
        while '<profession>' in result:
            result = result.replace('<profession>', self._random_profession(), 1)
        
        # Capitalize first letter of the headline
        if result:
            result = result[0].upper() + result[1:]
        
        return result
    
    def generate(self, count: int = 1) -> List[str]:
        """Generate the specified number of clickbait headlines."""
        headlines = []
        for _ in range(count):
            template = random.choice(self.templates)
            headline = self._fill_template(template)
            headlines.append(headline)
        return headlines


def generate_image(api_key: str, headline: str, post_slug: str) -> tuple:
    """Generate an image using DALL-E and save it locally. Returns tuple of (full_image_path, preview_image_path)."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The openai package is required. Install it with 'pip install openai'.")
    
    from PIL import Image
    from io import BytesIO
    
    client = OpenAI(api_key=api_key)
    
    # Create a prompt for DALL-E
    image_prompt = f"A bright, colorful, uplifting editorial illustration for a news article titled: {headline}. Style: modern digital art, vibrant, positive, suitable for a news website."
    
    # Generate image with DALL-E
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    
    # Download the image
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    
    # Save to assets/images/
    images_dir = 'assets/images'
    os.makedirs(images_dir, exist_ok=True)
    image_filename = f"{images_dir}/{post_slug}.png"
    preview_filename = f"{images_dir}/{post_slug}-preview.png"
    
    # Save full image
    with open(image_filename, 'wb') as f:
        f.write(image_response.content)
    
    # Create preview (300x300)
    img = Image.open(BytesIO(image_response.content))
    img.thumbnail((300, 300), Image.Resampling.LANCZOS)
    img.save(preview_filename, 'PNG')
    
    return image_filename, preview_filename


def call_openai_api(api_key: str, model: str, prompt: str, headlines: list,
                    author_name: str | None = None,
                    author_bio: str | None = None,
                    author_link: str | None = None) -> dict:
    """Send the prompt and headlines to OpenAI and return the response as dict. Supports openai>=1.0.0."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The openai package is required. Install it with 'pip install openai'.")
    client = OpenAI(api_key=api_key)
    user_content = prompt + "\n\nHeadlines: " + json.dumps(headlines)
    # Inject author context so the model can add a byline linking to About page
    if author_name and author_link:
        user_content += (
            "\n\nAuthor Context (for byline):\n"
            f"author_name: {author_name}\n"
            f"author_bio: {author_bio or ''}\n"
            f"author_link: {author_link}\n"
            "Instruction: The story string MUST begin with a single markdown byline line in the exact form\n"
            "By [AUTHOR_NAME](AUTHOR_LINK)\n"
            "Replace AUTHOR_NAME and AUTHOR_LINK with the provided values. Add a blank line after the byline, then the story."
        )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a creative and positive news reporter in the tabloid tradition writing clickbait stories. Always return your response as valid JSON with properly escaped strings."},
            {"role": "user", "content": user_content}
        ],
        max_tokens=1200,
        temperature=0.8
    )
    # Extract the content from the response
    content = response.choices[0].message.content
    
    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith('```'):
        # Remove markdown code fences
        lines = content.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    try:
        # Try parsing with strict=False to allow control characters
        return json.loads(content, strict=False)
    except json.JSONDecodeError as e:
        # If that fails, try to fix common issues
        print(f"\n=== Attempting to repair JSON ===")
        # The issue is that the story field contains literal newlines
        # We need to parse it differently
        try:
            import ast
            # Try using ast.literal_eval as a fallback
            return ast.literal_eval(content)
        except:
            print(f"JSON Parse Error: {e}")
            print(f"Content preview: {content[:200]}")
            raise


def slugify(value):
    """Convert a string to a URL-friendly slug."""
    value = value.lower()
    value = re.sub(r'[^a-z0-9\s-]', '', value)
    value = re.sub(r'\s+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')


def main():
    parser = argparse.ArgumentParser(
        description='Generate random clickbait headlines and create a story using OpenAI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --openai_key sk-... --model gpt-4 --count 5
        """
    )
    parser.add_argument('-n', '--nouns', default='nouns.txt', help='File containing nouns (default: nouns.txt)')
    parser.add_argument('-a', '--adjectives', default='adjectives.txt', help='File containing adjectives (default: adjectives.txt)')
    parser.add_argument('-v', '--verbs', default='verbs.txt', help='File containing verbs (default: verbs.txt)')
    parser.add_argument('-c', '--celebrities', default='celebrities.txt', help='File containing celebrity names (default: celebrities.txt)')
    parser.add_argument('-p', '--professions', default='professions.txt', help='File containing professions (default: professions.txt)')
    parser.add_argument('-t', '--templates', default='templates.txt', help='File containing headline templates (default: templates.txt)')
    parser.add_argument('--count', type=int, default=1, help='Number of headlines to generate (default: 1)')
    parser.add_argument('--openai_key', required=True, help='OpenAI API key')
    parser.add_argument('--model', default='gpt-4.1-nano', help='OpenAI model to use (default: gpt-4.1-nano)')
    args = parser.parse_args()

    try:
        # Define author bios and IDs to link to anchors on the About page
        AUTHORS = [
            {
                "name": "Bubbles McSprinkles",
                "id": "bubbles-mcsprinkles",
                "bio": (
                    "Chief Correspondent & Former Circus Unicyclist. "
                    "Spent fifteen years dazzling crowds juggling flaming pineapples while reciting Shakespeare. "
                    "World-record bubble-wrap popper; advocate for garden gnome rights."
                ),
            },
            {
                "name": "Duckie Quackers",
                "id": "duckie-quackers",
                "bio": (
                    "Senior Reporter & Professional Duck Feeder. "
                    "Aquatic choreography pioneer behind 'Swan Lake (But With Actual Ducks)'. "
                    "Breadcrumb trajectory researcher and rubber duck enthusiast."
                ),
            },
            {
                "name": "Sir Reginald Fluffington III",
                "id": "sir-reginald-fluffington-iii",
                "bio": (
                    "Investigative Journalist & Retired Pillow Fort Architect. "
                    "Designer of the triple-decker pillow fort with chocolate fountain. "
                    "Leads global inquiry into the mysterious disappearance of socks."
                ),
            },
            {
                "name": "Carlos \"The Cloud\" Ramirez",
                "id": "carlos-the-cloud-ramirez",
                "bio": (
                    "Weather Correspondent & Professional Cloud Watcher. "
                    "Cataloged 10,000+ cloud shapes and verifies rainbow plausibility on-site."
                ),
            },
            {
                "name": "Dr. Priya Whiskerworth",
                "id": "dr-priya-whiskerworth",
                "bio": (
                    "Science & Technology Editor & Professional Cat Translator. "
                    "Fluent in seventeen purr dialects; reports on speculative science (mostly snacks)."
                ),
            },
        ]
        generator = ClickbaitGenerator(
            nouns_file=args.nouns,
            adjectives_file=args.adjectives,
            verbs_file=args.verbs,
            celebrities_file=args.celebrities,
            professions_file=args.professions,
            templates_file=args.templates
        )
        headlines = generator.generate(args.count)
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")
        
        # Always send 5 headlines if possible
        selected_headlines = headlines[:5] if len(headlines) >= 5 else headlines
        
        # Load the story prompt
        with open('story_prompt.txt', 'r', encoding='utf-8') as f:
            story_prompt = f.read().strip()
        
        # Pick a random author and build their public link (include baseurl for GitHub Pages)
        author = random.choice(AUTHORS)
        author_link = f"/clickbait_generator/about.html#{author['id']}"

        # Call OpenAI API with author context so the story includes a byline
        story_response = call_openai_api(
            args.openai_key,
            args.model,
            story_prompt,
            selected_headlines,
            author_name=author["name"],
            author_bio=author["bio"],
            author_link=author_link,
        )
        
        # Prepare Jekyll post
        post_title = story_response['headline']
        post_slug = slugify(post_title)
        post_date = datetime.now().strftime('%Y-%m-%d')
        post_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
        
        # Generate image with DALL-E
        print("Generating image with DALL-E...")
        image_path, preview_path = generate_image(args.openai_key, post_title, post_slug)
        image_url = f"/assets/images/{post_slug}.png"
        preview_url = f"/assets/images/{post_slug}-preview.png"
        print(f"Image saved to {image_path}")
        print(f"Preview saved to {preview_path}")
        
        # Get summary
        summary = story_response.get('summary', '')
        
        post_dir = '_posts'
        os.makedirs(post_dir, exist_ok=True)
        post_filename = f"{post_dir}/{post_date}-{post_slug}.md"
        
        # Create Jekyll front matter
        front_matter = f"""---
layout: post
title: "{post_title}"
date: {post_datetime}
categories: articles
image: {image_url}
preview_image: {preview_url}
summary: "{summary}"
author: "{author['name']}"
author_url: "{author_link}"
---

![{post_title}]({{{{ '{image_url}' | relative_url }}}})

"""
        
        # Write the post file
        with open(post_filename, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(story_response['story'].lstrip())

        print(f"Story saved to {post_filename}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
