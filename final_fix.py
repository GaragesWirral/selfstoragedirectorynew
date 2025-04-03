import os
import shutil
import re
from bs4 import BeautifulSoup
import glob

def normalize_path(path):
    """Normalize a path to be used in URLs"""
    # Convert spaces and special characters to dashes
    path = re.sub(r'[^a-zA-Z0-9]', '-', path).lower()
    return path

def get_selfstorage_path(path):
    """Convert a path to include selfstorage prefix if needed"""
    # Normalize the path first
    normalized = normalize_path(path)
    
    # Check if it already has the prefix
    if normalized.startswith('selfstorage'):
        return normalized
    
    # Add prefix
    return 'selfstorage' + normalized

def update_html_content(content, depth=0):
    """Update HTML content with new paths and links"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Build the relative path prefix based on depth
    rel_prefix = '../' * depth
    
    # Update navigation links
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href:
            # Handle homepage link
            if href == '/' or href == '/index.html':
                a_tag['href'] = rel_prefix + 'index.html'
            
            # Handle absolute internal links
            elif href.startswith('/') and not href.startswith('//'):
                # Strip leading slash and add relative prefix
                href = href.lstrip('/')
                a_tag['href'] = rel_prefix + href
                
            # Update .html links to folder/index.html format
            if href.endswith('.html') and not href.startswith('http'):
                base_path = href.replace('.html', '')
                if base_path != 'index':  # Don't change index.html
                    a_tag['href'] = rel_prefix + base_path + '/index.html'
    
    # Update CSS paths
    for link_tag in soup.find_all('link', href=True):
        href = link_tag.get('href')
        if href.startswith('/assets/'):
            link_tag['href'] = rel_prefix + href.lstrip('/')
        elif href.startswith('assets/'):
            link_tag['href'] = rel_prefix + href
    
    # Update script paths
    for script_tag in soup.find_all('script', src=True):
        src = script_tag.get('src')
        if src.startswith('/assets/'):
            script_tag['src'] = rel_prefix + src.lstrip('/')
        elif src.startswith('assets/'):
            script_tag['src'] = rel_prefix + src
    
    # Update image paths
    for img_tag in soup.find_all('img', src=True):
        src = img_tag.get('src')
        if src.startswith('/assets/'):
            img_tag['src'] = rel_prefix + src.lstrip('/')
        elif src.startswith('assets/'):
            img_tag['src'] = rel_prefix + src
    
    return str(soup)

def process_html_file(file_path, new_path=None, depth=0):
    """Process an HTML file, update links, and save to new location"""
    # Ensure the directory exists
    if new_path:
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
    
    # Read the HTML content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Update the content
    updated_content = update_html_content(content, depth)
    
    # Save to new location
    target_path = new_path if new_path else file_path
    with open(target_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print(f"Processed {file_path} -> {target_path}")

def cleanup_directories():
    """Remove directories with duplicate selfstorage prefixes"""
    print("Cleaning up directories with duplicate prefixes...")
    root_path = 'website'
    
    # Find all directories that start with "selfstorageselfstorage"
    for dir_name in os.listdir(root_path):
        dir_path = os.path.join(root_path, dir_name)
        if os.path.isdir(dir_path) and dir_name.startswith('selfstorageselfstorage'):
            print(f"Found directory with duplicate prefix: {dir_name}")
            
            # Create a fixed name by removing one "selfstorage" prefix
            fixed_name = dir_name.replace('selfstorageselfstorage', 'selfstorage')
            fixed_path = os.path.join(root_path, fixed_name)
            
            # Check if the properly named directory already exists
            if not os.path.exists(fixed_path):
                print(f"  Renaming to: {fixed_name}")
                os.makedirs(fixed_path, exist_ok=True)
                
                # Copy all files and subdirectories 
                for item in os.listdir(dir_path):
                    item_src = os.path.join(dir_path, item)
                    item_dst = os.path.join(fixed_path, item)
                    if os.path.isdir(item_src):
                        if not item.startswith('selfstorage'):
                            # Fix subdirectory names too
                            fixed_subdir = 'selfstorage' + item
                            item_dst = os.path.join(fixed_path, fixed_subdir)
                        try:
                            shutil.copytree(item_src, item_dst)
                            print(f"    Copied directory: {item} -> {os.path.basename(item_dst)}")
                        except Exception as e:
                            print(f"    Error copying directory {item}: {e}")
                    else:
                        try:
                            shutil.copy2(item_src, item_dst)
                            print(f"    Copied file: {item}")
                        except Exception as e:
                            print(f"    Error copying file {item}: {e}")

def fix_html_links():
    """Fix links in HTML files to use the corrected structure"""
    print("Fixing HTML links in all files...")
    root_path = 'website'
    
    # Process all HTML files
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Determine depth based on path
                depth = len(os.path.relpath(file_path, root_path).split(os.sep)) - 1
                
                # Process the file in place
                process_html_file(file_path, None, depth)

def main():
    """Main function to fix the website structure"""
    # Step 1: Clean up directories with duplicate prefixes
    cleanup_directories()
    
    # Step 2: Fix HTML links to use the corrected structure
    fix_html_links()
    
    print("Website structure fixed successfully!")

if __name__ == "__main__":
    main() 