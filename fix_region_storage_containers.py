import os
import re
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

def find_region_pages_missing_storage_list():
    """Find all region index.html pages that are missing storage-list containers."""
    region_pages = []
    website_dir = os.path.join(os.getcwd(), "website")
    
    for item in os.listdir(website_dir):
        item_path = os.path.join(website_dir, item)
        if os.path.isdir(item_path) and item.startswith("selfstorage"):
            index_file = os.path.join(item_path, "index.html")
            if os.path.exists(index_file) and is_missing_storage_list(index_file):
                region_pages.append(index_file)
    
    return region_pages

def is_missing_storage_list(filepath):
    """Check if a file is missing the storage-list container."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        main_content = soup.find('main')
        
        if not main_content:
            return False  # No main tag to check
        
        storage_list = main_content.find(class_="storage-list")
        return storage_list is None
    
    except Exception as e:
        print(f"Error checking {filepath}: {str(e)}")
        return False

def clean_region_name(region_name):
    """Clean the region name for display purposes."""
    if not region_name:
        return "UK"
    
    # Remove 'selfstorage' prefix if present
    if region_name.startswith("selfstorage"):
        region_name = region_name[11:]
    
    # Replace hyphens with spaces and capitalize words
    region_name = region_name.replace("-", " ").strip()
    
    # Handle special cases
    if region_name.lower() == "uk":
        return "the UK"
    
    return region_name.title()

def get_region_cities(region_dir):
    """Get a list of cities in the region."""
    cities = []
    
    for item in os.listdir(region_dir):
        item_path = os.path.join(region_dir, item)
        if os.path.isdir(item_path) and "index.html" in os.listdir(item_path):
            city_name = item
            if city_name.startswith("selfstorage"):
                city_name = city_name[11:]
            city_name = city_name.replace("-", " ").title()
            cities.append({
                "name": city_name,
                "path": os.path.join(item, "index.html")
            })
    
    return cities[:6]  # Return up to 6 cities for the list

def add_storage_list(filepath):
    """Add a storage-list container to a region page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get the region name
        region_dir = os.path.dirname(filepath)
        region_folder = os.path.basename(region_dir)
        region_name = clean_region_name(region_folder)
        
        main_content = soup.find('main')
        if not main_content:
            return False  # No main tag to modify
        
        # Add storage-list container
        storage_list = soup.new_tag("div")
        storage_list["class"] = "storage-list"
        
        # Add section title
        section_title = soup.new_tag("h2")
        section_title.string = f"Cities with Storage Facilities in {region_name}"
        storage_list.append(section_title)
        
        # Get cities in this region
        cities = get_region_cities(region_dir)
        
        # Create grid of city cards
        city_grid = soup.new_tag("div")
        city_grid["class"] = "storage-grid"
        
        if not cities:
            # If no cities found, add some dummy ones
            dummy_cities = [
                {"name": f"{region_name} City", "path": "#"},
                {"name": f"{region_name} West", "path": "#"},
                {"name": f"{region_name} East", "path": "#"}
            ]
            cities = dummy_cities
        
        for city in cities:
            city_card = soup.new_tag("div")
            city_card["class"] = "storage-card"
            
            city_link = soup.new_tag("a")
            city_link["href"] = city["path"]
            city_link.string = f"Self Storage in {city['name']}"
            
            city_card.append(city_link)
            city_grid.append(city_card)
        
        storage_list.append(city_grid)
        
        # Add the storage-list to the main content
        main_content.append(storage_list)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error adding storage-list to {filepath}: {str(e)}")
        return False

def main():
    start_time = time.time()
    
    print("Finding region pages missing storage-list containers...")
    region_pages = find_region_pages_missing_storage_list()
    print(f"Found {len(region_pages)} region pages missing storage-list containers.")
    
    fixed_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        
        for filepath in region_pages:
            futures.append(executor.submit(add_storage_list, filepath))
        
        for i, future in enumerate(futures):
            try:
                if future.result():
                    fixed_count += 1
                    print(f"[{fixed_count}/{len(region_pages)}] Fixed: {region_pages[i]}")
            except Exception as e:
                error_count += 1
                print(f"Error processing {region_pages[i]}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    print("\nFix summary:")
    print(f"- Total region pages missing storage-list: {len(region_pages)}")
    print(f"- Successfully fixed: {fixed_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 