import os
from datetime import datetime

def update_copyright_year():
    """
    Updates the copyright year in the footer across all HTML files
    """
    website_dir = 'website'
    current_year = datetime.now().year
    updated_count = 0
    
    # Walk through all subdirectories of the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Replace the copyright year
                if '© 2024 Storage Finder' in content:
                    content = content.replace('© 2024 Storage Finder', f'© {current_year} Storage Finder')
                    updated_count += 1
                    
                    # Write the updated content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
    
    print(f"Updated copyright year to {current_year} on {updated_count} pages")

if __name__ == "__main__":
    update_copyright_year() 