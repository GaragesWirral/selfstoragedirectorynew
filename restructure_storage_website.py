import os
import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import glob

# Base directory for the website
website_dir = 'website'

# Create missing directories if they don't exist
def create_directories():
    # Create folders for the top-level HTML files
    folders = ['faq', 'about', 'contact', 'privacy', 'terms', 'membership', 'selfstorageregions']
    for folder in folders:
        folder_path = os.path.join(website_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
    # Create new assets folder or keep existing one
    assets_path = os.path.join(website_dir, 'assets')
    os.makedirs(os.path.join(assets_path, 'css'), exist_ok=True)
    os.makedirs(os.path.join(assets_path, 'js'), exist_ok=True)

# Helper functions to transform paths and update links
def to_selfstorage_path(path):
    """Convert region names to selfstorage format."""
    # Check if the path already has the selfstorage prefix
    if path.startswith('selfstorage'):
        return path
    
    # Convert spaces and special characters to dashes
    path = re.sub(r'[^a-zA-Z0-9]', '-', path).lower()
    # Add selfstorage prefix
    return 'selfstorage' + path

def update_html_content(content, depth=0):
    """Update links and paths in HTML content based on folder depth"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Update stylesheet link based on depth
    css_path = "../" * depth + "assets/css/style.css"
    for link in soup.find_all('link', rel='stylesheet'):
        if 'style.css' in link.get('href', ''):
            link['href'] = css_path
    
    # Update navigation links
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')
        if not href:
            continue
            
        # Skip external links or anchors
        if href.startswith(('http', 'mailto', '#')):
            continue
            
        # Update root links in the navigation - using relative paths based on depth
        if href == 'index.html':
            # For homepage links, use relative paths based on depth
            if depth == 0:
                a_tag['href'] = 'index.html'
            else:
                a_tag['href'] = '../' * depth + 'index.html'
        elif href == 'regions.html':
            # For regions page links
            if depth == 0:
                a_tag['href'] = 'selfstorageregions/index.html'
            else:
                a_tag['href'] = '../' * depth + 'selfstorageregions/index.html'
        elif href.endswith('.html'):
            # Convert name.html to name/index.html
            base_name = os.path.splitext(os.path.basename(href))[0]
            dir_name = os.path.dirname(href)
            
            if dir_name:
                # Handle paths like ../name.html
                path_parts = dir_name.split('/')
                new_parts = []
                
                for part in path_parts:
                    if part == '..':
                        new_parts.append('..')
                    elif part:
                        new_parts.append(to_selfstorage_path(part))
                
                new_dir = '/'.join(new_parts)
                if new_dir:
                    a_tag['href'] = f"{new_dir}/{base_name}/index.html"
                else:
                    a_tag['href'] = f"{base_name}/index.html"
            else:
                # Handle simple cases like name.html
                if depth == 0:
                    a_tag['href'] = f"{base_name}/index.html"
                else:
                    a_tag['href'] = f"../{'../' * (depth-1)}{base_name}/index.html"
        
        # Update region and city links
        elif '/index.html' in href:
            # If href starts with a slash, remove it for relative paths
            if href.startswith('/'):
                href = href[1:]
                
            dir_path = href.replace('/index.html', '')
            path_parts = dir_path.split('/')
            new_parts = []
            
            for part in path_parts:
                if part == '..':
                    new_parts.append('..')
                elif part:
                    new_parts.append(to_selfstorage_path(part))
            
            new_path = '/'.join(new_parts)
            
            # Calculate relative path based on depth
            if depth > 0 and not href.startswith('../'):
                relative_prefix = '../' * depth
                a_tag['href'] = f"{relative_prefix}{new_path}/index.html"
            else:
                a_tag['href'] = f"{new_path}/index.html"
    
    # Update JavaScript search redirects
    for script in soup.find_all('script'):
        if script.string and "window.location.href" in script.string:
            # Replace regions.html redirects
            script.string = script.string.replace(
                "window.location.href = 'regions.html", 
                "window.location.href = 'selfstorageregions/index.html"
            )
            
            # Replace absolute path redirects with relative paths
            script.string = script.string.replace(
                "window.location.href = '/", 
                "window.location.href = '"
            )
            
            # Other redirects with .html extension
            for match in re.findall(r"window\.location\.href\s*=\s*['\"](.*?)\.html", script.string):
                if match != 'index':
                    script.string = script.string.replace(
                        f"window.location.href = '{match}.html", 
                        f"window.location.href = '{match}/index.html"
                    )
    
    return str(soup)

def process_html_file(file_path, new_path=None, depth=0):
    """Process an HTML file, update its content, and move it to the new location"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = update_html_content(content, depth)
    
    # If no new path is provided, update in place
    save_path = new_path if new_path else file_path
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def restructure_website():
    """Main function to restructure the website."""
    print("Starting website restructuring...")
    root_path = 'website'
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    # Create new directories
    create_directories()
    
    # First pass: Process top-level HTML files in the root
    print("Processing top-level HTML files...")
    for html_file in glob.glob('*.html'):
        if html_file != 'index.html':  # Skip homepage for now
            new_folder = html_file.replace('.html', '')
            new_path = os.path.join(root_path, new_folder, 'index.html')
            process_html_file(html_file, new_path, depth=1)
            print(f"  Moved {html_file} to {new_path}")
    
    # Process homepage
    print("Processing homepage...")
    if os.path.exists('index.html'):
        new_path = os.path.join(root_path, 'index.html')
        process_html_file('index.html', new_path, depth=0)
        print(f"  Moved index.html to {new_path}")
    
    # Second pass: Process region directories
    print("Processing region directories...")
    for dir_path in glob.glob('*'):
        if os.path.isdir(dir_path) and dir_path != 'website' and not dir_path.startswith('.'):
            # Skip directories that already have selfstorage prefix to avoid double-prefixing
            if not os.path.basename(dir_path).startswith('selfstorage'):
                region_name = os.path.basename(dir_path)
                new_region_name = to_selfstorage_path(region_name)
                new_region_path = os.path.join(root_path, new_region_name)
                
                print(f"Processing region: {region_name} -> {new_region_name}")
                
                if not os.path.exists(new_region_path):
                    os.makedirs(new_region_path)
                
                # Process region's index.html
                region_index = os.path.join(dir_path, 'index.html')
                if os.path.exists(region_index):
                    new_path = os.path.join(new_region_path, 'index.html')
                    process_html_file(region_index, new_path, depth=1)
                    print(f"  Moved {region_index} to {new_path}")
                
                # Process city directories within the region
                for city_dir in glob.glob(os.path.join(dir_path, '*')):
                    if os.path.isdir(city_dir):
                        city_name = os.path.basename(city_dir)
                        new_city_name = to_selfstorage_path(city_name)
                        new_city_path = os.path.join(new_region_path, new_city_name)
                        
                        print(f"  Processing city: {city_name} -> {new_city_name}")
                        
                        if not os.path.exists(new_city_path):
                            os.makedirs(new_city_path)
                        
                        # Process city's index.html
                        city_index = os.path.join(city_dir, 'index.html')
                        if os.path.exists(city_index):
                            new_path = os.path.join(new_city_path, 'index.html')
                            process_html_file(city_index, new_path, depth=2)
                            print(f"    Moved {city_index} to {new_path}")
    
    # Move regions.html to selfstorageregions/index.html
    if os.path.exists('regions.html'):
        new_path = os.path.join(root_path, 'selfstorageregions', 'index.html')
        process_html_file('regions.html', new_path, depth=1)
        print(f"Moved regions.html to {new_path}")
    
    print("Website restructuring completed!")
    
    # Clean up old files
    cleanup_old_files()

def cleanup_old_files():
    """Remove old files and directories after restructuring."""
    print("Cleaning up old files...")
    
    # Remove top-level HTML files
    for html_file in glob.glob('*.html'):
        try:
            os.remove(html_file)
            print(f"Removed {html_file}")
        except Exception as e:
            print(f"Could not remove {html_file}: {e}")
    
    # Remove old region directories
    for item in glob.glob('*'):
        if os.path.isdir(item) and item != 'website' and not item.startswith('.'):
            try:
                print(f"Attempting to remove directory: {item}")
                
                # Skip .git directories
                for root, dirs, files in os.walk(item, topdown=True):
                    dirs[:] = [d for d in dirs if d != '.git']
                    
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            print(f"  Removed file: {file_path}")
                        except Exception as e:
                            print(f"  Could not remove file {file_path}: {e}")
                
                # Try to remove the directory after clearing files
                try:
                    os.rmdir(item)
                    print(f"Removed directory: {item}")
                except Exception as e:
                    print(f"Could not remove directory {item}: {e}")
                    
            except Exception as e:
                print(f"Error processing directory {item}: {e}")
    
    print("Cleanup completed!")

if __name__ == "__main__":
    restructure_website() 