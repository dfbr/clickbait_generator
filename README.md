# Clickbait Story Generator

An automated clickbait headline and story generator that creates complete articles with images and publishes them to a Jekyll-based GitHub Pages site. The system uses OpenAI's GPT models to generate engaging stories from clickbait headlines, and DALL-E 3 to create custom images for each article.

🌐 **Live Site**: [https://dfbr.github.io/clickbait_generator/](https://dfbr.github.io/clickbait_generator/)

## Features

### Content Generation
- 15+ different clickbait headline templates (easily customizable)
- OpenAI GPT-4 integration for complete story generation
- DALL-E 3 image generation for each article
- Automatic preview thumbnails (300x300) for the index page
- 20-30 word summary teasers for each story
- Customizable word lists (nouns, adjectives, verbs, celebrities, professions)
- External prompt file for easy story generation customization

### Website Features
- Automated Jekyll static site on GitHub Pages
- Modern card-based grid layout for the index page
- Responsive design with tabloid-style red theme (#c8102e)
- Individual article pages with full-size images
- Daily automated story generation via GitHub Actions
- SEO-optimized with Jekyll plugins

### Automation
- GitHub Actions workflow for daily story generation (3 AM GMT)
- Manual workflow dispatch for on-demand generation
- Automatic git commits and pushes
- Built-in virtual environment support

## Installation

### Prerequisites
- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git and GitHub account (for deployment)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dfbr/clickbait_generator.git
cd clickbait_generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install openai requests Pillow
```

4. Set up your OpenAI API key as a GitHub secret:
   - Go to your repository Settings → Secrets and variables → Actions
   - Create a new secret named `OPENAI_API_KEY`
   - Paste your OpenAI API key as the value

## Usage

### Local Story Generation

Generate a single story with OpenAI integration:
```bash
python clickbait_generator.py --openai_key YOUR_API_KEY --model gpt-4
```

Generate multiple stories:
```bash
python clickbait_generator.py --count 5 --openai_key YOUR_API_KEY --model gpt-4
```

### Testing Jekyll Site Locally

1. Install Jekyll (requires Ruby):
```bash
gem install jekyll bundler
```

2. Serve the site locally:
```bash
jekyll serve
```

3. Visit `http://localhost:4000/clickbait_generator/` in your browser

### Automated Daily Generation

The GitHub Actions workflow runs automatically every day at 3 AM GMT, generating a new story and publishing it to the site. You can also trigger it manually:

1. Go to the Actions tab in your GitHub repository
2. Select "Generate Daily Story"
3. Click "Run workflow"

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--nouns` | `-n` | File containing nouns | `nouns.txt` |
| `--adjectives` | `-a` | File containing adjectives | `adjectives.txt` |
| `--verbs` | `-v` | File containing verbs | `verbs.txt` |
| `--celebrities` | `-c` | File containing celebrity names | `celebrities.txt` |
| `--professions` | `-p` | File containing professions | `professions.txt` |
| `--templates` | `-t` | File containing headline templates | `templates.txt` |
| `--count` | | Number of stories to generate | `1` |
| `--openai_key` | | OpenAI API key (required for story generation) | None |
| `--model` | | OpenAI model to use | `gpt-4` |

## File Structure

```
clickbait_generator/
├── clickbait_generator.py    # Main Python script
├── story_prompt.txt           # OpenAI prompt template
├── templates.txt              # Headline templates
├── nouns.txt                  # Noun word list
├── adjectives.txt             # Adjective word list
├── verbs.txt                  # Verb word list
├── celebrities.txt            # Celebrity/character names
├── professions.txt            # Profession word list
├── _config.yml                # Jekyll configuration
├── _layouts/                  # Jekyll layout templates
│   ├── default.html          # Main layout with header/footer
│   └── post.html             # Individual article layout
├── _posts/                    # Generated story markdown files
├── assets/
│   ├── images/
│   │   ├── logo.png          # Site logo
│   │   ├── favicon.ico       # Site favicon
│   │   └── posts/            # Generated article images
│   │       └── previews/     # 300x300 thumbnail images
│   └── style.css             # Custom CSS styling
├── index.md                   # Homepage with story grid
├── about.md                   # About page
└── .github/workflows/
    └── generate-story.yml     # Automated daily generation
```

## How It Works

### Story Generation Process

1. **Headline Creation**: The script randomly selects a template and fills it with words from the word lists
2. **Story Generation**: The headline is sent to OpenAI GPT-4 with a custom prompt requesting:
   - A complete story (3-5 paragraphs)
   - A 20-30 word summary teaser
   - All returned as JSON
3. **Image Generation**: DALL-E 3 creates a vivid, dramatic illustration based on the headline
4. **Thumbnail Creation**: A 300x300 preview image is generated using Pillow (PIL)
5. **Jekyll Post Creation**: A markdown file is created in `_posts/` with:
   - Front matter (title, date, image URLs, summary, etc.)
   - Full story content
6. **Git Commit**: Changes are automatically committed and pushed to GitHub
7. **Site Deployment**: GitHub Pages automatically rebuilds and deploys the site

### OpenAI Integration

The system uses two OpenAI APIs:
- **GPT-4** (or gpt-4-turbo): Generates the story content and summary
- **DALL-E 3**: Creates HD (1792×1024) images for each story

The story prompt (`story_prompt.txt`) instructs the model to write uplifting, feel-good stories with vivid details and positive messages.

### Image Generation

Images are saved in two formats:
- **Full size**: `assets/images/posts/YYYY-MM-DD-slug.png` (1792×1024)
- **Preview**: `assets/images/posts/previews/YYYY-MM-DD-slug.png` (300×300)

Preview images are displayed on the homepage in the story grid, while full-size images appear on individual article pages.

## Customization

### Modifying Word Lists

Edit any of the `.txt` word list files. Each file should contain one word or phrase per line:

```
word1
word2 with spaces
word3
```

### Customizing Headline Templates

Edit `templates.txt` to add or modify headline templates. Available placeholders:

- `<number>` - Random number (1-100, weighted towards clickbait values)
- `<percentage>` - Random percentage (1-99, for quiz-style headlines)
- `<adjective>` - Random adjective from your list
- `<noun>` - Random noun from your list
- `<verb>` - Random verb from your list
- `<celebrity>` - Random celebrity/character from your list
- `<profession>` - Random profession from your list

Example templates:
```
<number> <adjective> <noun> That Will <verb> Your Mind
You Won't Believe What This <adjective> <noun> Can Do!
<celebrity>'s Secret to <adjective> <noun> Revealed!
```

### Customizing the Story Prompt

Edit `story_prompt.txt` to change how stories are generated. The prompt should instruct the model to return JSON with three fields:
- `headline` - The exact clickbait headline
- `story` - The full story text (3-5 paragraphs)
- `summary` - A 20-30 word teaser for the homepage

### Customizing Site Appearance

- **Colors/Styling**: Edit `assets/style.css`
- **Layout**: Modify files in `_layouts/`
- **Homepage**: Edit `index.md`
- **Site Title/Description**: Update `_config.yml`

## GitHub Actions Workflow

The automated workflow (`.github/workflows/generate-story.yml`) runs daily and:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies (openai, requests, Pillow)
4. Runs the generator script with the OpenAI API key from secrets
5. Commits new posts and images
6. Pushes changes to GitHub
7. Triggers automatic GitHub Pages deployment

You can modify the schedule by editing the cron expression:
```yaml
schedule:
  - cron: '0 3 * * *'  # Every day at 3 AM GMT
```

## Included Headline Templates

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

## Technical Details

### Dependencies

- **openai** (≥1.0.0): OpenAI API client for GPT-4 and DALL-E 3
- **requests**: HTTP library for downloading generated images
- **Pillow**: Image processing for creating preview thumbnails

### OpenAI API Costs

Approximate costs per story (as of 2025):
- GPT-4 story generation: ~$0.01-0.03 per story
- DALL-E 3 HD image: ~$0.08 per image
- **Total per story**: ~$0.09-0.11

Running daily = ~$2.70-3.30/month

### Jekyll Configuration

Key settings in `_config.yml`:
- `baseurl: "/clickbait_generator"` - Subdirectory for GitHub Pages
- `future: true` - Allows posts with future dates to be published
- `permalink: /articles/:year/:month/:day/:title.html` - URL structure
- Plugins: `jekyll-feed`, `jekyll-seo-tag`

## Deployment

### GitHub Pages Setup

1. Push your repository to GitHub
2. Go to Settings → Pages
3. Set Source to "Deploy from a branch"
4. Select branch: `main`, folder: `/ (root)`
5. Click Save

Your site will be available at: `https://[username].github.io/clickbait_generator/`

### Setting Up Automation

1. Add your OpenAI API key to repository secrets:
   - Settings → Secrets and variables → Actions
   - New repository secret: `OPENAI_API_KEY`

2. Verify the workflow has write permissions:
   - Settings → Actions → General
   - Workflow permissions: "Read and write permissions"

3. The workflow will run automatically at 3 AM GMT daily

## Example Output

### Generated Headline
```
7 Shocking Secrets About Quantum Coffee That Will Transform Your Mind
```

### Generated Story Structure
```markdown
---
layout: post
title: "7 Shocking Secrets About Quantum Coffee That Will Transform Your Mind"
date: 2025-11-03 15:30:00 +0000
image: /clickbait_generator/assets/images/posts/2025-11-03-quantum-coffee.png
preview_image: /clickbait_generator/assets/images/posts/previews/2025-11-03-quantum-coffee.png
summary: "Discover how scientists unlocked the mind-bending properties of quantum-enhanced coffee beans that defy reality itself."
---

[3-5 paragraphs of uplifting story content]
```

### Homepage Display
- Card grid layout with preview images (300×300)
- Story title as clickable link
- Summary teaser (20-30 words)
- Publication date
- Hover effects and responsive design

## Troubleshooting

### OpenAI API Errors

- **Authentication failed**: Check your API key is correct and has available credits
- **Model not found**: Ensure you have access to GPT-4 and DALL-E 3 (may require paid account)
- **Rate limit**: The API has rate limits; space out multiple generations

### Jekyll Build Errors

- **Posts not showing**: Check `future: true` is set in `_config.yml`
- **Images not loading**: Verify `baseurl` is correct in `_config.yml`
- **CSS not applying**: Clear browser cache and check file paths

### GitHub Actions Failures

- **Permission denied**: Ensure workflow has write permissions in repository settings
- **Secret not found**: Verify `OPENAI_API_KEY` is added to repository secrets
- **Python errors**: Check all dependencies are listed in workflow file

## Contributing

Feel free to submit issues and pull requests! Ideas for enhancement:

- Additional headline templates
- More word lists (locations, emotions, etc.)
- Different story styles (horror, sci-fi, etc.)
- Multi-language support
- Story archives by month/category
- RSS feed enhancements

## License

Free to use and modify!

## Acknowledgments

- OpenAI for GPT-4 and DALL-E 3 APIs
- Jekyll for static site generation
- GitHub Pages for free hosting
- The wonderful world of clickbait for inspiration 🎉
