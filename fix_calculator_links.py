import os
import re

def fix_calculator_links():
    """
    Fixes calculator links on all pages and removes duplicate calculator links
    """
    # Directory to search for HTML files
    website_dir = 'website'
    
    # Counters for modified pages
    fixed_links = 0
    removed_duplicates = 0
    
    # Walk through all subdirectories of the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                
                # Skip the calculator page itself
                if 'calculator/index.html' in file_path:
                    # Only check for duplicates on calculator page
                    pass
                else:
                    # 1. Calculate depth relative to website root for proper relative path
                    rel_path = os.path.relpath(root, website_dir)
                    
                    # Fix path based on depth from root
                    if rel_path == '.':
                        # We're at the website root
                        calc_path = 'calculator/index.html'
                    else:
                        # Count directories to go up
                        levels_up = len(rel_path.split(os.sep))
                        calc_path = '../' * levels_up + 'calculator/index.html'
                    
                    # Replace all paths to calculator, even if they're already somewhat correct
                    # This brute force approach should fix all variations
                    content = re.sub(
                        r'href="[\.\/]*calculator/index\.html"', 
                        f'href="{calc_path}"', 
                        content
                    )
                    
                    fixed_links += 1
                    modified = True
                
                # 2. Remove duplicate calculator links in navigation
                nav_pattern = r'<nav>\s*<ul>(.*?)</ul>\s*</nav>'
                nav_match = re.search(nav_pattern, content, re.DOTALL)
                
                if nav_match:
                    nav_content = nav_match.group(1)
                    
                    # Check for duplicate calculator links
                    calc_item_pattern = r'<li><a href="[^"]*">Storage Calculator</a></li>'
                    calc_items = re.findall(calc_item_pattern, nav_content)
                    
                    if len(calc_items) > 1:
                        # Keep only the first calculator link
                        fixed_nav = nav_content
                        # We need to remove duplicates but keep the original
                        for i in range(1, len(calc_items)):
                            fixed_nav = fixed_nav.replace(calc_items[i], '')
                        
                        # Replace the navigation content
                        content = content.replace(nav_match.group(1), fixed_nav)
                        removed_duplicates += 1
                        modified = True
                
                # Write the updated content back to the file if modified
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
    
    print(f"Fixed calculator links on {fixed_links} pages")
    print(f"Removed duplicate calculator links on {removed_duplicates} pages")

if __name__ == "__main__":
    fix_calculator_links() 