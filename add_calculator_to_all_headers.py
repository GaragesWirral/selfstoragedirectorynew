import os
import re

def add_calculator_to_all_headers():
    """
    Adds the Storage Calculator link to the header navigation on all website pages
    """
    # Directory to search for HTML files
    website_dir = 'website'
    
    # Pattern to find the navigation UL in the header
    nav_pattern = r'<nav>\s*<ul>(.*?)</ul>\s*</nav>'
    
    # Pattern to check if calculator link already exists
    calculator_check = r'calculator/index.html">Storage Calculator'
    
    # Counter for modified pages
    modified_pages = 0
    
    # Walk through all subdirectories of the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Skip if calculator link already exists
                if re.search(calculator_check, content):
                    continue
                
                # Find the navigation section
                nav_match = re.search(nav_pattern, content, re.DOTALL)
                if nav_match:
                    nav_content = nav_match.group(1)
                    
                    # Calculate the relative path to the calculator page
                    # First, get the relative depth
                    depth = file_path.replace(website_dir, '').count(os.sep)
                    relative_path = '../' * depth if depth > 0 else ''
                    if depth == 0:  # If in root directory
                        calc_link = 'calculator/index.html'
                    else:
                        calc_link = f'{relative_path}calculator/index.html'
                    
                    # Create new navigation with calculator link
                    new_nav = nav_content + f'\n<li><a href="{calc_link}">Storage Calculator</a></li>'
                    
                    # Replace old navigation with new navigation
                    content = content.replace(nav_match.group(1), new_nav)
                    
                    # Write the updated content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    modified_pages += 1
    
    print(f"Successfully added Storage Calculator link to {modified_pages} pages!")

if __name__ == "__main__":
    add_calculator_to_all_headers() 