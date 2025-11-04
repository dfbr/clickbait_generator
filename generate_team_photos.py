#!/usr/bin/env python3
"""Generate team member photos using DALL-E"""

from openai import OpenAI
import requests
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate team member photos')
    parser.add_argument('--openai_key', required=True, help='OpenAI API key')
    args = parser.parse_args()
    
    client = OpenAI(api_key=args.openai_key)

    reporters = [
        {
            'name': 'Bubbles McSprinkles',
            'prompt': 'Professional headshot photo of a cheerful young East Asian woman in colorful circus attire with sparkles, former unicyclist, bright and energetic personality, studio portrait, high quality',
            'filename': 'bubbles-mcsprinkles.png'
        },
        {
            'name': 'Duckie Quackers',
            'prompt': 'Professional headshot photo of a friendly Black woman wearing duck-themed accessories, professional duck feeder, warm smile, natural hair, studio portrait, high quality',
            'filename': 'duckie-quackers.png'
        },
        {
            'name': 'Sir Reginald Fluffington III',
            'prompt': 'Professional headshot photo of a distinguished elderly white man with a mustache in fancy pajamas or robe, retired pillow fort architect, sophisticated yet cozy appearance, studio portrait, high quality',
            'filename': 'sir-reginald-fluffington.png'
        },
        {
            'name': 'Carlos "The Cloud" Ramirez',
            'prompt': 'Professional headshot photo of a confident Latino man in his 30s wearing weather-related accessories, former professional cloud watcher, enthusiastic expression, studio portrait, high quality',
            'filename': 'carlos-ramirez.png'
        },
        {
            'name': 'Dr. Priya Whiskerworth',
            'prompt': 'Professional headshot photo of a South Asian woman in her 40s wearing cat-themed jewelry, professional cat translator, intelligent and warm expression, glasses, studio portrait, high quality',
            'filename': 'priya-whiskerworth.png'
        }
    ]

    os.makedirs('assets/images/team', exist_ok=True)

    for reporter in reporters:
        print(f"Generating image for {reporter['name']}...")
        response = client.images.generate(
            model='dall-e-3',
            prompt=reporter['prompt'],
            size='1024x1024',
            quality='standard',
            n=1
        )
        
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        
        filepath = os.path.join('assets', 'images', 'team', reporter['filename'])
        with open(filepath, 'wb') as f:
            f.write(img_data)
        
        print(f'Saved {filepath}')

    print('All reporter photos generated successfully!')

if __name__ == '__main__':
    main()

