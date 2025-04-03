import os
import re
from pathlib import Path

def fix_blog_links():
    """
    Fixes incorrectly added blog links in the header navigation
    """
    # Directory to search for HTML files
    website_dir = 'website'
    
    # Counter for fixed pages
    fixed_pages = 0
    
    # Walk through all subdirectories of the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Remove incorrectly placed blog links
                incorrect_pattern = r'</ul>\s*</nav>\s*<li><a href="[^"]*">Blog</a></li></ul></nav>'
                if re.search(incorrect_pattern, content):
                    # Fix the content by removing the incorrect link
                    new_content = re.sub(incorrect_pattern, '</ul></nav>', content)
                    
                    # Determine the correct path based on file location
                    blog_path = "../blog/index.html"
                    if "website" == os.path.basename(root):
                        blog_path = "blog/index.html"
                    
                    # Find the last list item in the navigation and insert the blog link
                    nav_pattern = r'(<li><a href="[^"]*">[^<]*</a></li>)\s*</ul>\s*</nav>'
                    nav_match = re.search(nav_pattern, new_content)
                    
                    if nav_match:
                        # Properly insert the new list item before the closing </ul>
                        last_item = nav_match.group(1)
                        replacement = last_item + f'\n<li><a href="{blog_path}">Blog</a></li></ul></nav>'
                        new_content = new_content.replace(nav_match.group(0), replacement)
                    
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_pages += 1
    
    print(f"Fixed blog links on {fixed_pages} pages")

if __name__ == "__main__":
    fix_blog_links() 