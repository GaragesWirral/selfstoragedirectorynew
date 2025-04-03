import os
import re
from bs4 import BeautifulSoup

# Bedford styling - this will be applied to all other city pages
BEDFORD_STYLE = """
    .storage-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    
    .storage-card {
        background-color: white;
        border: 1px solid #28A745;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .storage-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.2);
    }
    
    .storage-card h3 {
        color: #006400;
        font-size: 22px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e9ecef;
    }
    
    .storage-info {
        display: grid;
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .contact-info {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #e9ecef;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .contact-info p {
        margin-bottom: 5px;
    }
    
    .contact-info a {
        color: #006400;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }
    
    .contact-info a:hover {
        color: #28A745;
        text-decoration: underline;
    }
    
    .features-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 15px;
    }
    
    .feature-tag {
        background-color: #e8f5e9;
        color: #006400;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
    }
"""

def find_city_pages():
    """Find all city HTML pages in the website directory structure."""
    city_pages = []
    for root, dirs, files in os.walk("website"):
        for file in files:
            if file == "index.html" and "selfstorage" in root and "selfstorageregions" not in root:
                # Check if it's a city page (subdirectory of a region)
                parts = root.split(os.sep)
                if len(parts) >= 3:
                    # This is likely a city page
                    city_pages.append(os.path.join(root, file))
    
    return city_pages

def apply_consistent_styling(filepath):
    """Apply the Bedford styling to a city page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # Check if this is a city page with storage facilities
        storage_list = soup.select_one('.storage-list')
        if not storage_list:
            print(f"Skipping {filepath} - not a city page with storage-list")
            return False
        
        # Find the style tag or create one if it doesn't exist
        style_tag = soup.select_one('head style')
        if not style_tag:
            # Create a new style tag
            style_tag = soup.new_tag('style')
            # Add it to the head
            head = soup.select_one('head')
            if head:
                head.append(style_tag)
            else:
                print(f"Skipping {filepath} - no head tag found")
                return False
        
        # Update the style content
        style_tag.string = BEDFORD_STYLE
        
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Updated styling for {filepath}")
        return True
    
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Main function to find and update all city pages."""
    city_pages = find_city_pages()
    print(f"Found {len(city_pages)} city pages to update")
    
    # Print first few to debug
    for page in city_pages[:3]:
        print(f"Sample page: {page}")
    
    # Apply consistent styling to all pages
    updated_count = 0
    for page in city_pages:
        if apply_consistent_styling(page):
            updated_count += 1
    
    print(f"Updated styling for {updated_count} out of {len(city_pages)} city pages")

if __name__ == "__main__":
    main() 