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

                        def slugify(value):
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
                            parser.add_argument('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
                            args = parser.parse_args()

                            try:
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
                                # Call OpenAI API
                                story_response = call_openai_api(args.openai_key, args.model, story_prompt, selected_headlines)
                                # Prepare Jekyll post
                                post_title = story_response['headline']
                                post_slug = slugify(post_title)
                                post_date = datetime.now().strftime('%Y-%m-%d')
                                post_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
                                post_dir = '_posts'
                                os.makedirs(post_dir, exist_ok=True)
                                post_filename = f"{post_dir}/{post_date}-{post_slug}.md"
                                front_matter = f"""---
        """Get a random celebrity name."""
        return random.choice(self.celebrities)
    
    def _random_profession(self) -> str:
        return random.choice(self.professions)
                                with open(post_filename, 'w', encoding='utf-8') as f:
                                    f.write(front_matter)
                                    f.write(story_response['story'].lstrip())
                                print(f"Story saved to {post_filename}")
                            except Exception as e:
                                print(f"Error: {e}")
                                return 1
                            return 0
    
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



def call_openai_api(api_key: str, model: str, prompt: str, headlines: list) -> dict:
    """Send the prompt and headlines to OpenAI and return the response as dict. Supports openai>=1.0.0."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("The openai package is required. Install it with 'pip install openai'.")
    client = OpenAI(api_key=api_key)
    user_content = prompt + "\n\nHeadlines: " + json.dumps(headlines)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a creative and positive storyteller."},
            {"role": "user", "content": user_content}
        ],
        max_tokens=1200,
        temperature=0.8
    )
    # Extract the content from the response
    content = response.choices[0].message.content
    return json.loads(content)


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
    parser.add_argument('--model', default='gpt-4', help='OpenAI model to use (default: gpt-4)')
    args = parser.parse_args()

    try:
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
        # Call OpenAI API
        story_response = call_openai_api(args.openai_key, args.model, story_prompt, selected_headlines)
        # Save the story as markdown
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{now}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {story_response['headline']}\n\n{story_response['story']}")
        print(f"Story saved to {filename}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == '__main__':
    exit(main())
