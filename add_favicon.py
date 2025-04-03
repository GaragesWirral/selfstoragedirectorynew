import os
import re

def add_favicon_to_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if favicon already exists
    if 'rel="icon"' in content:
        return
    
    # Calculate relative path to assets
    rel_path = os.path.relpath('website/assets', os.path.dirname(file_path)).replace('\\', '/')
    if not rel_path.startswith('.'):
        rel_path = './' + rel_path
    
    # Prepare favicon links
    favicon_links = f'''<link rel="icon" type="image/png" sizes="32x32" href="{rel_path}/img/favicon-32x32.png"/>
<link rel="icon" type="image/png" sizes="16x16" href="{rel_path}/img/favicon-16x16.png"/>'''
    
    # Add favicon links after meta description
    content = re.sub(
        r'(<meta[^>]*description[^>]*>)',
        r'\1\n' + favicon_links,
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                add_favicon_to_file(file_path)

if __name__ == "__main__":
    process_directory('website') 