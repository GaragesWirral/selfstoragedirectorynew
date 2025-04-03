import os
import re
from pathlib import Path

def add_blog_link_to_headers():
    """
    Adds a blog link to the header navigation on all website pages
    """
    # Directory to search for HTML files
    website_dir = 'website'
    
    # Counter for modified pages
    modified_pages = 0
    skipped_pages = 0
    
    # Walk through all subdirectories of the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Skip if blog link already exists in navigation
                if '<a href="../blog/index.html">Blog</a>' in content or '<a href="blog/index.html">Blog</a>' in content:
                    skipped_pages += 1
                    continue
                
                # Determine the correct path based on file location
                blog_path = "../blog/index.html"
                if "website" == os.path.basename(root):
                    blog_path = "blog/index.html"
                
                # Find the last list item in the navigation
                nav_pattern = r'(<li><a href="[^"]*">[^<]*</a></li>)\s*</ul>\s*</nav>'
                nav_match = re.search(nav_pattern, content)
                
                if nav_match:
                    # Properly insert the new list item before the closing </ul>
                    last_item = nav_match.group(1)
                    replacement = last_item + f'\n<li><a href="{blog_path}">Blog</a></li></ul></nav>'
                    new_content = content.replace(nav_match.group(0), replacement)
                    
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    modified_pages += 1
    
    print(f"Added blog link to {modified_pages} pages")
    print(f"Skipped {skipped_pages} pages (already had blog link)")

if __name__ == "__main__":
    add_blog_link_to_headers() 