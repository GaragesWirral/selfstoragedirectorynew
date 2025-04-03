import os
import shutil
import re
from bs4 import BeautifulSoup
import glob
from pathlib import Path

def create_directories():
    """Create the necessary directories for the website structure"""
    print("Creating necessary directories...")
    root_path = 'website'
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    # Create directory for assets
    assets_path = os.path.join(root_path, 'assets')
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)
        os.makedirs(os.path.join(assets_path, 'css'))
        os.makedirs(os.path.join(assets_path, 'js'))
    
    # Create directories for top-level pages
    for page in ['about', 'faq', 'contact', 'privacy', 'terms', 'membership', 'selfstorageregions']:
        page_path = os.path.join(root_path, page)
        if not os.path.exists(page_path):
            os.makedirs(page_path)
    
    print("Directories created successfully.")

def to_selfstorage_path(path):
    """Convert a path to selfstorage format, avoiding duplicates"""
    # Normalize path
    path = re.sub(r'[^a-zA-Z0-9]', '-', str(path)).lower()
    
    # Check if it already has the prefix
    if path.startswith('selfstorage'):
        return path
    
    # Add prefix
    return 'selfstorage' + path

def update_html_content(content, depth=0):
    """Update HTML content with relative paths for local viewing"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Build the relative path prefix
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
                # Strip leading slash and add relative path
                href = href.lstrip('/')
                a_tag['href'] = rel_prefix + href
            
            # Update links that end with .html
            if href.endswith('.html') and not href.startswith('http'):
                base_path = href.replace('.html', '')
                if base_path != 'index':  # Don't change index.html
                    a_tag['href'] = rel_prefix + base_path + '/index.html'
    
    # Update CSS and JS paths
    for tag in soup.find_all(['link', 'script'], href=True):
        href = tag.get('href')
        if href and (href.startswith('/assets/') or href.startswith('assets/')):
            tag['href'] = rel_prefix + href.lstrip('/')
    
    # Update script src paths
    for script_tag in soup.find_all('script', src=True):
        src = script_tag.get('src')
        if src and (src.startswith('/assets/') or src.startswith('assets/')):
            script_tag['src'] = rel_prefix + src.lstrip('/')
    
    # Update image paths
    for img_tag in soup.find_all('img', src=True):
        src = img_tag.get('src')
        if src and (src.startswith('/assets/') or src.startswith('assets/')):
            img_tag['src'] = rel_prefix + src.lstrip('/')
    
    return str(soup)

def process_html_file(file_path, new_path=None, depth=0):
    """Process an HTML file, update links, and save to new location"""
    # Ensure the directory exists for the new path
    if new_path:
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
    
    try:
        # Read the HTML content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update the content
        updated_content = update_html_content(content, depth)
        
        # Save to new location or overwrite existing
        target_path = new_path if new_path else file_path
        with open(target_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"Processed {file_path} -> {target_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def restructure_website():
    """Restructure the website with the correct paths"""
    print("Starting website restructuring...")
    root_path = 'website'
    
    # Step 1: Create necessary directories
    create_directories()
    
    # Step 2: Process top-level HTML files
    print("Processing top-level HTML files...")
    for html_file in glob.glob('*.html'):
        if html_file != 'index.html':  # Skip homepage for now
            folder_name = html_file.replace('.html', '')
            new_path = os.path.join(root_path, folder_name, 'index.html')
            process_html_file(html_file, new_path, depth=1)
    
    # Process homepage
    if os.path.exists('index.html'):
        homepage_path = os.path.join(root_path, 'index.html')
        process_html_file('index.html', homepage_path, depth=0)
        print(f"Processed index.html -> {homepage_path}")
    
    # Step 3: Process region folders
    print("Processing region directories...")
    for dir_path in glob.glob('*'):
        if os.path.isdir(dir_path) and not dir_path.startswith('.') and dir_path != 'website':
            region_name = os.path.basename(dir_path)
            new_region_name = to_selfstorage_path(region_name)
            new_region_path = os.path.join(root_path, new_region_name)
            
            print(f"Processing region: {region_name} -> {new_region_name}")
            
            # Process region index.html
            region_index = os.path.join(dir_path, 'index.html')
            if os.path.exists(region_index):
                new_index_path = os.path.join(new_region_path, 'index.html')
                process_html_file(region_index, new_index_path, depth=1)
            
            # Process city directories
            for city_dir in [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]:
                city_path = os.path.join(dir_path, city_dir)
                new_city_name = to_selfstorage_path(city_dir)
                new_city_path = os.path.join(new_region_path, new_city_name)
                
                print(f"  Processing city: {city_dir} -> {new_city_name}")
                
                # Process city index.html
                city_index = os.path.join(city_path, 'index.html')
                if os.path.exists(city_index):
                    new_city_index_path = os.path.join(new_city_path, 'index.html')
                    process_html_file(city_index, new_city_index_path, depth=2)
    
    # Step 4: Process regions.html specially
    if os.path.exists('regions.html'):
        regions_path = os.path.join(root_path, 'selfstorageregions', 'index.html')
        process_html_file('regions.html', regions_path, depth=1)
    
    print("Website restructuring completed successfully!")

if __name__ == "__main__":
    # Execute the restructuring
    restructure_website() 