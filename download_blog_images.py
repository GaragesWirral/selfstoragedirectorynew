import os
import requests
from urllib.parse import urljoin

# Create the blog images directory if it doesn't exist
os.makedirs('website/assets/img/blog', exist_ok=True)

# Sample images for blog posts
images = {
    'organizing-tips.jpg': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80',
    'security-features.jpg': 'https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=80',
    'insurance-guide.jpg': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80',
    'climate-control.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&q=80'
}

# Download each image
for filename, url in images.items():
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join('website/assets/img/blog', filename), 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')
    else:
        print(f'Failed to download {filename}') 