import os
import re

def add_ontoplist_badge(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if badge already exists
    if 'ontoplist.com' in content:
        print(f"Skipping {file_path} - badge already exists")
        return
    
    # Add badge before closing footer tag
    badge_html = '''
    <div class="ontoplist-badge" style="text-align: center; margin-top: 20px;">
        <a href="https://ontoplist.com/self-storage-directory/" target="_blank">
            <img src="https://ontoplist.com/images/badges/ontoplist-badge.png" alt="OnToplist Badge" style="max-width: 200px; height: auto;">
        </a>
    </div>'''
    
    # Replace closing footer tag with badge + closing tag
    new_content = content.replace('</footer>', f'{badge_html}</footer>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added badge to {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                add_ontoplist_badge(file_path)

if __name__ == '__main__':
    process_directory('website') 