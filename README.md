# Clickbait Headline Generator

A Python script that generates random clickbait headlines using customizable word lists and multiple template styles.

## Features

- 15+ different clickbait headline templates (easily customizable)
- Templates stored in external file for easy editing
- Customizable word lists (nouns, adjectives, verbs, celebrities)
- Randomly generated numbers (1-100) with clickbait-friendly weighting
- Smart percentage generation for quiz-style headlines
- Command-line interface with configurable options
- Generate multiple headlines at once
- Default word list files included

## Installation

No external dependencies required! Just Python 3.6+.

```bash
# Clone or download this repository
cd clickBait
```

## Usage

### Basic Usage

Generate a single headline (default):
```bash
python clickbait_generator.py
```

### Generate Multiple Headlines

```bash
python clickbait_generator.py --count 5
```

### Custom Word Lists

Specify your own word list files:
```bash
python clickbait_generator.py --nouns my_nouns.txt --adjectives my_adjectives.txt
```

Short form:
```bash
python clickbait_generator.py -n my_nouns.txt -a my_adj.txt -v my_verbs.txt
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--nouns` | `-n` | File containing nouns | `nouns.txt` |
| `--adjectives` | `-a` | File containing adjectives | `adjectives.txt` |
| `--verbs` | `-v` | File containing verbs | `verbs.txt` |
| `--celebrities` | `-c` | File containing celebrity names | `celebrities.txt` |
| `--professions` | `-p` | File containing professions | `professions.txt` |
| `--templates` | `-t` | File containing headline templates | `templates.txt` |
| `--count` | | Number of headlines to generate | `1` |

**Note**: Numbers are generated randomly (1-100) with preference for clickbait-friendly values like 3, 5, 7, 10, etc.

## Creating Custom Templates

You can create your own headline templates by editing `templates.txt` or creating a new template file. Templates use the following placeholders:

- `<number>` - Random number (1-100, weighted towards clickbait values)
- `<percentage>` - Random percentage (1-99, for quiz-style headlines)
- `<adjective>` - Random adjective from your list
- `<noun>` - Random noun from your list
- `<verb>` - Random verb from your list
- `<celebrity>` - Random celebrity/character from your list
- `<profession>` - Random profession from your list

### Template File Format

```
# Lines starting with # are comments
# Blank lines are ignored

<number> <adjective> <noun> That Will <verb> Your Mind
You Won't Believe What This <adjective> <noun> Can Do!
<profession> Hate This <adjective> <noun>! Here's Why
<celebrity>'s Secret to <adjective> <noun> Revealed!
```

Each placeholder can appear multiple times in a template and will be replaced with a different random value each time.

## Headline Templates

The generator includes 15 different clickbait styles:

1. **Number-based listicle**: "X Adjective Nouns That Will Verb Your Mind"
2. **You won't believe**: "You Won't Believe What This Adjective Noun Can Do!"
3. **Shocking revelation**: "This Adjective Noun Will Verb Everything You Know About Noun"
4. **Doctors/Scientists hate**: "Doctors Hate This Adjective Noun! Here's Why"
5. **Celebrity numbered list**: "X Times Celebrity Was Caught Verbing a Noun"
6. **What happened next**: "They Verbed a Adjective Noun. What Happened Next Will Verb You!"
7. **One simple trick**: "One Adjective Trick to Verb Your Noun..."
8. **Number reasons why**: "X Reasons Why Noun Is More Adjective Than You Think"
9. **Quiz style**: "Only X% of People Can Verb This Adjective Noun. Can You?"
10. **Before and after**: "She Verbed Her Noun and You Won't Believe What It Looks Like Now!"
11. **Celebrity secret**: "Celebrity's Secret to Adjective Noun Revealed!"
12. **Scientists discovered**: "Scientists Just Discovered a Adjective Way to Verb Noun!"
13. **Life-changing**: "This Adjective Noun Changed My Life in X Days"
14. **Shocking truth**: "The Adjective Truth About Noun That Nobody Tells You"
15. **Things you didn't know**: "X Things You Didn't Know About Adjective Noun"

## Word List Format

Each word list file should contain one word/phrase per line:

```
word1
word2
word3
```

## Example Output

```
10 Shocking Secrets That Will Change Your Mind
You Won't Believe What This Amazing Smartphone Can Do!
Scientists Hate This Revolutionary Diet! Here's Why
7 Times Elon Musk Was Caught Improving a Coffee
The Hidden Truth About Pizza That Nobody Tells You
```

## Future Development

This project is planned to integrate with OpenAI to generate actual stories based on these clickbait headlines.

## License

Free to use and modify!
