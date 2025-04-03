import os
import re

def remove_ontoplist_badge(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if badge exists
    if 'ontoplist.com' not in content:
        print(f"Skipping {file_path} - no badge found")
        return
    
    # Remove the badge div and its contents
    pattern = r'\s*<div class="ontoplist-badge"[^>]*>.*?</div>'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Removed badge from {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                remove_ontoplist_badge(file_path)

if __name__ == '__main__':
    process_directory('website') 