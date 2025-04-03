import os
from bs4 import BeautifulSoup
import re

def make_links_nofollow(file_path):
    """Make website links nofollow and non-clickable in a single HTML file."""
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    # Read HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all website links (but not email or phone links)
    links = soup.find_all('a')
    modified = False
    
    for link in links:
        href = link.get('href', '')
        # Only process website links (not email or phone)
        if href.startswith('https://') or href.startswith('http://'):
            # Add rel="nofollow" attribute
            link['rel'] = 'nofollow'
            
            # Store the original href as a data attribute
            link['data-original-href'] = href
            
            # Change href to prevent clicking
            link['href'] = 'javascript:void(0);'
            
            # Add title attribute to show it's not clickable
            if not link.has_attr('title'):
                link['title'] = 'Link disabled for security reasons'
            
            modified = True
    
    if modified:
        # Save the modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    
    return False

def process_directory(directory_path):
    """Process all HTML files in a directory and its subdirectories."""
    count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if make_links_nofollow(file_path):
                    count += 1
                    print(f"Updated links in {file_path}")
    
    return count

if __name__ == "__main__":
    # Process the entire website directory
    website_dir = 'website'
    
    if os.path.exists(website_dir):
        modified_count = process_directory(website_dir)
        print(f"\nSummary: Modified {modified_count} HTML files to make website links nofollow and non-clickable")
    else:
        print(f"Website directory not found: {website_dir}") 