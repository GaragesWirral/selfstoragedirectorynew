import os
import re
from bs4 import BeautifulSoup

def add_about_storage_section():
    """
    Add an "About Storage" section to every city page, similar to the one in Bedford.
    The section will be added before the footer.
    """
    website_dir = 'website'
    modified_count = 0
    
    # Walk through all directories and files in the website directory
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            # Only process index.html files in city subdirectories
            if file == 'index.html' and len(root.split(os.path.sep)) > 2:
                # Skip region index files
                if root.count(os.path.sep) < 2:
                    continue
                
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
                
                # Check if the About Storage section already exists
                existing_about = soup.find('h2', string='About Storage in')
                if existing_about:
                    continue  # Skip if section already exists
                
                # Extract city name from the path
                path_parts = root.split(os.path.sep)
                city_dir = path_parts[-1]
                city_name = city_dir.replace('selfstorage', '')
                
                # Format city name (convert hyphens to spaces and capitalize first letter of each word)
                city_name = city_name.replace('-', ' ').title()
                
                # Create the About Storage section
                about_div = soup.new_tag('div', style="margin-top: 40px;")
                about_h2 = soup.new_tag('h2')
                about_h2.string = f"About Storage in {city_name}"
                about_div.append(about_h2)
                
                about_p1 = soup.new_tag('p')
                about_p1.string = f"{city_name} offers a variety of self storage options to meet different needs, from household storage during moves to business inventory management. Most facilities provide secure, clean units with various access options and additional services like packing supplies and delivery acceptance."
                about_div.append(about_p1)
                
                about_p2 = soup.new_tag('p')
                about_p2.string = f"When choosing a storage facility in {city_name}, consider factors like location, access hours, security features, and whether climate control is needed for sensitive items. Many facilities offer flexible contracts with monthly payments, and some provide special discounts for long-term storage."
                about_div.append(about_p2)
                
                # Find the storage-list div to insert after
                storage_list = soup.find('div', class_='storage-list')
                
                if storage_list:
                    # Find the parent container of the storage-list
                    container = storage_list.parent
                    container.append(about_div)
                    
                    # Save the modified content
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        modified_count += 1
                        print(f"Added About Storage section to {file_path}")
                    except Exception as e:
                        print(f"Error writing to {file_path}: {e}")
    
    print(f"\nSummary: Added About Storage section to {modified_count} city pages")

if __name__ == "__main__":
    add_about_storage_section() 