#!/usr/bin/env python3
"""
Clickbait Headline Generator
Generates random clickbait headlines using templates and word lists.
"""

import argparse
import random
from pathlib import Path
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
        
        # Define clickbait headline templates
        self.templates = [
            # Template 1: Number-based listicle
            lambda: f"{self._random_number()} {self._random_adjective()} {self._random_noun()} That Will {self._random_verb()} Your Mind",
            
            # Template 2: You won't believe
            lambda: f"You Won't Believe What This {self._random_adjective()} {self._random_noun()} Can Do!",
            
            # Template 3: Shocking revelation
            lambda: f"This {self._random_adjective()} {self._random_noun()} Will {self._random_verb()} Everything You Know About {self._random_noun()}",
            
            # Template 4: Doctors/Scientists hate
            lambda: f"Doctors Hate This {self._random_adjective()} {self._random_noun()}! Here's Why",
            
            # Template 5: Number with celebrity
            lambda: f"{self._random_number()} Times {self._random_celebrity()} Was Caught {self._random_verb()} a {self._random_noun()}",
            
            # Template 6: What happened next
            lambda: f"They {self._random_verb()} a {self._random_adjective()} {self._random_noun()}. What Happened Next Will {self._random_verb()} You!",
            
            # Template 7: One simple trick
            lambda: f"One {self._random_adjective()} Trick to {self._random_verb()} Your {self._random_noun()} That {self._random_adjective()} Companies Don't Want You to Know",
            
            # Template 8: Number reasons why
            lambda: f"{self._random_number()} Reasons Why {self._random_noun()} Is More {self._random_adjective()} Than You Think",
            
            # Template 9: Quiz style
            lambda: f"Only {self._random_percentage()}% of People Can {self._random_verb()} This {self._random_adjective()} {self._random_noun()}. Can You?",
            
            # Template 10: Before and after
            lambda: f"She {self._random_verb()} Her {self._random_noun()} and You Won't Believe What It Looks Like Now!",
            
            # Template 11: Celebrity secret
            lambda: f"{self._random_celebrity()}'s Secret to {self._random_adjective()} {self._random_noun()} Revealed!",
            
            # Template 12: Industry professionals
            lambda: f"Scientists Just Discovered a {self._random_adjective()} Way to {self._random_verb()} {self._random_noun()}!",
            
            # Template 13: Life-changing
            lambda: f"This {self._random_adjective()} {self._random_noun()} Changed My Life in {self._random_number()} Days",
            
            # Template 14: Shocking truth
            lambda: f"The {self._random_adjective()} Truth About {self._random_noun()} That Nobody Tells You",
            
            # Template 15: Things you didn't know
            lambda: f"{self._random_number()} Things You Didn't Know About {self._random_adjective()} {self._random_noun()}",
        ]
    
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


def main():
    """Main entry point for the clickbait generator."""
    parser = argparse.ArgumentParser(
        description='Generate random clickbait headlines',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate 1 headline (default)
  %(prog)s --count 5                          # Generate 5 headlines
  %(prog)s --nouns my_nouns.txt               # Use custom nouns file
  %(prog)s -n my_nouns.txt -a my_adj.txt      # Use custom files
        """
    )
    
    parser.add_argument(
        '-n', '--nouns',
        default='nouns.txt',
        help='File containing nouns (default: nouns.txt)'
    )
    parser.add_argument(
        '-a', '--adjectives',
        default='adjectives.txt',
        help='File containing adjectives (default: adjectives.txt)'
    )
    parser.add_argument(
        '-v', '--verbs',
        default='verbs.txt',
        help='File containing verbs (default: verbs.txt)'
    )
    parser.add_argument(
        '-c', '--celebrities',
        default='celebrities.txt',
        help='File containing celebrity names (default: celebrities.txt)'
    )
    parser.add_argument(
        '-p', '--professions',
        default='professions.txt',
        help='File containing professions (default: professions.txt)'
    )
    parser.add_argument(
        '-t', '--templates',
        default='templates.txt',
        help='File containing headline templates (default: templates.txt)'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of headlines to generate (default: 1)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create generator
        generator = ClickbaitGenerator(
            nouns_file=args.nouns,
            adjectives_file=args.adjectives,
            verbs_file=args.verbs,
            celebrities_file=args.celebrities,
            professions_file=args.professions,
            templates_file=args.templates
        )
        
        # Generate headlines
        headlines = generator.generate(args.count)
        
        # Output headlines
        for i, headline in enumerate(headlines, 1):
            if args.count > 1:
                print(f"{i}. {headline}")
            else:
                print(headline)
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
