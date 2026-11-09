# Clickbait Story Generator

An automated clickbait story generator that creates complete articles with images and publishes them to a Jekyll-based GitHub Pages site. Everything is written by AI: an OpenAI GPT model invents the headline and writes the story, summary, categories and the illustration brief in a single request, and gpt-image-1-mini draws the picture from that brief.

🌐 **Live Site**: [https://clickbait.dfbr.co.uk](https://clickbait.dfbr.co.uk)

## Features

### Content Generation
- Headlines, stories, summaries, categories, image prompts and alt text all written by the LLM (gpt-6-luna by default)
- Only two API calls per story: one text call (structured JSON output) and one image call
- gpt-image-1-mini image generation for each article, in a style the LLM picks for the story
- Automatic preview thumbnails (300x300) for the index page
- Recent headlines are passed to the model so it doesn't repeat itself
- External prompt file (`story_prompt.txt`) for easy customization

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

Generate a story:
```bash
python clickbait_generator.py --openai_key YOUR_API_KEY
```

Generate the text only (no image call; the image prompt is printed instead):
```bash
python clickbait_generator.py --openai_key YOUR_API_KEY --no-images
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

3. Visit `http://localhost:4000/` in your browser

### Automated Daily Generation

The GitHub Actions workflow runs automatically every day at 3 AM GMT, generating a new story and publishing it to the site. You can also trigger it manually:

1. Go to the Actions tab in your GitHub repository
2. Select "Generate Daily Story"
3. Click "Run workflow"

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--openai_key` | | OpenAI API key (or set `OPENAI_API_KEY`) | None |
| `--model` | | OpenAI model to use | `gpt-6-luna` |
| `--prompt` | | Story prompt file | `story_prompt.txt` |
| `--no-images` | | Skip image generation and use placeholders | off |

## File Structure

```
clickbait_generator/
├── clickbait_generator.py    # Main Python script
├── story_prompt.txt           # OpenAI prompt template
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

1. **Story Generation (one LLM call)**: The prompt, a randomly chosen author's bio, the allowed categories and the site's recent headlines are sent to OpenAI (gpt-6-luna by default). Using structured outputs, the model returns JSON containing:
   - An original clickbait headline it invented
   - The full story (300-700 words, markdown)
   - A 20-30 word summary teaser
   - One or two categories from `_data/categories.json`
   - A complete image-generation prompt (the model picks the art style) and alt text
2. **Image Generation (one image call)**: gpt-image-1-mini draws the illustration from the model's image prompt
3. **Thumbnail Creation**: A 300x300 preview image is generated using Pillow (PIL)
4. **Jekyll Post Creation**: A markdown file is created in `_posts/` with:
   - Front matter (title, date, image URLs, summary, etc.)
   - Full story content
5. **Git Commit**: Changes are automatically committed and pushed to GitHub
6. **Site Deployment**: GitHub Pages automatically rebuilds and deploys the site

### OpenAI Integration

The system uses two OpenAI APIs:
- **gpt-6-luna** (default; override with `--model`): Generates the headline, story, summary, categories and image prompt in one call
- **gpt-image-1-mini**: Creates images for each story

The story prompt (`story_prompt.txt`) instructs the model to write uplifting, feel-good stories with vivid details and positive messages.

### Image Generation

Images are saved in two formats:
- **Full size**: `assets/images/posts/YYYY-MM-DD-slug.png` (1792×1024)
- **Preview**: `assets/images/posts/previews/YYYY-MM-DD-slug.png` (300×300)

Preview images are displayed on the homepage in the story grid, while full-size images appear on individual article pages.

## Customization

### Customizing the Story Prompt

Edit `story_prompt.txt` to change how headlines, stories and images are generated. The JSON fields the model must return (`headline`, `summary`, `categories`, `story`, `image_prompt`, `image_alt`) are enforced by the schema in `clickbait_generator.py`, so the prompt only needs to describe what goes in them.

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

## Technical Details

### Dependencies

- **openai** (≥1.0.0): OpenAI API client for the story model and gpt-image-1-mini
- **requests**: HTTP library for downloading generated images
- **Pillow**: Image processing for creating preview thumbnails

### OpenAI API Costs

Approximate costs per story (as of 2025):
- gpt-6-luna story generation: well under $0.01 per story
- gpt-image-1-mini image: ~$0.02 per image
- **Total per story**: ~$0.03-0.05

Running daily = ~$0.90-1.50/month

### Jekyll Configuration

Key settings in `_config.yml`:
- `baseurl: ""` - Empty when using a custom domain (site served from root)
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

Your site will be available at: `https://clickbait.dfbr.co.uk`

### Setting Up Automation

1. Add your OpenAI API key to repository secrets:
   - Settings → Secrets and variables → Actions
   - New repository secret: `OPENAI_API_KEY`

2. Verify the workflow has write permissions:
   - Settings → Actions → General
   - Workflow permissions: "Read and write permissions"

3. The workflow will run automatically at 3 AM GMT daily

## Example Output

### Generated Story Structure
```markdown
---
layout: post
title: "7 Shocking Secrets About Quantum Coffee That Will Transform Your Mind"
date: 2025-11-03 15:30:00 +0000
image: /assets/images/posts/2025-11-03-quantum-coffee.png
preview_image: /assets/images/posts/previews/2025-11-03-quantum-coffee.png
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
- **Model not found**: Ensure you have access to the chosen story model and gpt-image-1-mini (may require paid account)
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

- Different story styles (horror, sci-fi, etc.)
- Multi-language support
- Story archives by month/category
- RSS feed enhancements

## License

Free to use and modify!

## Acknowledgments

- OpenAI for the GPT and gpt-image-1-mini APIs
- Jekyll for static site generation
- GitHub Pages for free hosting
- The wonderful world of clickbait for inspiration 🎉
