import os
import re
from pathlib import Path

def update_footers():
    """Update all HTML files to add sitemap link to footer navigation"""
    website_dir = Path("website")
    
    # Counter for tracking changes
    files_updated = 0
    
    # Regular expression to match the navigation section in footer
    nav_pattern = re.compile(r'(<div class="footer-column"><h3>Navigate</h3><ul>.*?<li><a href=".*?faq/index.html">FAQ</a></li>)(</ul></div>)')
    
    # Replacement will vary based on whether it's the root or a subpage
    def replacement(match):
        if "href=\"../faq/index.html\"" in match.group(1):
            # Subpage
            return f'{match.group(1)}<li><a href="../sitemap/index.html">Sitemap</a></li>{match.group(2)}'
        else:
            # Root page
            return f'{match.group(1)}<li><a href="sitemap/index.html">Sitemap</a></li>{match.group(2)}'
    
    # Process all HTML files in the website directory and its subdirectories
    for root, _, files in os.walk(website_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # Read the HTML content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update the navigation section in footer
                updated_content = nav_pattern.sub(replacement, content)
                
                # If content was changed, write it back to the file
                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    files_updated += 1
                    print(f"Updated footer in: {file_path}")
    
    print(f"\nTotal files updated: {files_updated}")
    print("Footer update complete!")

if __name__ == "__main__":
    update_footers() 