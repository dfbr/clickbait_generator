from PIL import Image
import os
team_dir = os.path.join('assets', 'images', 'team')
files = sorted(os.listdir(team_dir))
for fn in files:
    path = os.path.join(team_dir, fn)
    try:
        with Image.open(path) as img:
            print(f"{fn}: {img.width}x{img.height}")
    except Exception as e:
        print(f"{fn}: ERROR - {e}")
