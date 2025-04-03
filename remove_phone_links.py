import os
import re
from bs4 import BeautifulSoup

def convert_phone_links_to_text():
    """
    Convert all phone links to plain text (remove anchor tags)
    """
    website_dir = 'website'
    modified_count = 0
    
    # Walk through all directories and files in the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Check if the file exists
                if not os.path.exists(file_path):
                    continue
                
                # Read the HTML file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
                
                # Parse the HTML
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all phone links in the "Phone: " section
                modified = False
                
                for label in soup.find_all('strong', string='Phone: '):
                    parent_p = label.parent
                    if parent_p:
                        # Find anchor tags in the parent paragraph
                        links = parent_p.find_all('a')
                        for link in links:
                            # Get the text from the link
                            phone_text = link.get_text()
                            # Replace the entire anchor tag with just the text
                            link.replace_with(phone_text)
                            modified = True
                
                if modified:
                    # Save the modified content
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        modified_count += 1
                        print(f"Converted phone links to text in {file_path}")
                    except Exception as e:
                        print(f"Error writing to {file_path}: {e}")
    
    print(f"\nSummary: Converted phone links to plain text in {modified_count} HTML files")

if __name__ == "__main__":
    convert_phone_links_to_text() 