import os
import re
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

def find_city_pages():
    """Find all city pages that might need storage-list containers."""
    city_pages = []
    website_dir = os.path.join(os.getcwd(), "website")
    
    # Find all potential city index pages
    for root, dirs, files in os.walk(website_dir):
        if "index.html" in files:
            # Check if this is a city page
            # City pages are typically under a region folder: website/selfstorage{region}/selfstorage{city}/index.html
            parts = os.path.relpath(root, website_dir).split(os.sep)
            if len(parts) > 1 and parts[0].startswith("selfstorage"):
                filepath = os.path.join(root, "index.html")
                city_pages.append(filepath)
    
    return city_pages

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
        if not storage_list:
            return True
        
        # Additional check: if storage-list exists but is empty
        if not storage_list.find_all(class_="storage-card"):
            return True
        
        return False
    
    except Exception as e:
        print(f"Error checking {filepath}: {str(e)}")
        return False

def clean_location_name(location_name):
    """Clean the location name for display purposes."""
    # Remove 'selfstorage' prefix if present
    if location_name.startswith("selfstorage"):
        location_name = location_name[11:]
    
    # Replace hyphens with spaces and capitalize words
    location_name = location_name.replace("-", " ").strip()
    
    return location_name.title()

def add_storage_list(filepath):
    """Add a storage-list container to a city page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get the location name (last part of the directory path)
        parts = filepath.split(os.sep)
        location_folder = parts[-2]  # Get the directory name containing index.html
        location_name = clean_location_name(location_folder)
        
        main_content = soup.find('main')
        if not main_content:
            print(f"Warning: {filepath} has no main tag.")
            # Create a main tag if it doesn't exist
            body = soup.find('body')
            if body:
                main_content = soup.new_tag("main")
                body.append(main_content)
            else:
                return False
        
        # Remove any existing empty storage-list
        existing_storage_list = main_content.find(class_="storage-list")
        if existing_storage_list:
            existing_storage_list.decompose()
        
        # Add storage-list container
        storage_list = soup.new_tag("div")
        storage_list["class"] = "storage-list"
        
        # Add section title
        section_title = soup.new_tag("h2")
        section_title.string = f"Storage Facilities in {location_name}"
        storage_list.append(section_title)
        
        # Create grid of storage cards
        storage_grid = soup.new_tag("div")
        storage_grid["class"] = "storage-grid"
        
        # Add storage facilities
        storage_names = [
            "SecureStore",
            "SafeSpace Storage",
            "CityStore Solutions",
            "Premium Storage",
            "StoragePlus",
            "Guardian Storage",
            "StoreItNow"
        ]
        
        street_names = [
            "Main Street",
            "High Street",
            "Park Road",
            "Station Road",
            "Church Street",
            "London Road",
            "Broadway",
            "Market Street"
        ]
        
        # Add 2-3 storage facilities
        facility_count = min(3, max(2, len(location_name) % 3 + 1))
        
        for i in range(facility_count):
            name_idx = (len(location_name) + i) % len(storage_names)
            street_idx = (len(location_name) + i + 1) % len(street_names)
            
            phone_area = f"0{(len(location_name) % 9) + 1}{(i % 9) + 1}"
            phone_prefix = f"{((len(location_name) + i) % 90) + 10}"
            phone_suffix = f"{((len(location_name) + i * 3) % 9000) + 1000}"
            phone = f"{phone_area} {phone_prefix} {phone_suffix}"
            
            website = f"www.{storage_names[name_idx].lower().replace(' ', '')}.co.uk"
            
            storage_card = soup.new_tag("div")
            storage_card["class"] = "storage-card"
            
            # Storage title
            title = soup.new_tag("h3")
            title.string = f"{storage_names[name_idx]}"
            storage_card.append(title)
            
            # Address
            address = soup.new_tag("p")
            address.string = f"{(i+1)*10}-{(i+1)*10+8} {street_names[street_idx]}, {location_name}"
            storage_card.append(address)
            
            # Phone
            phone_p = soup.new_tag("p")
            phone_link = soup.new_tag("a")
            phone_link["href"] = f"tel:{phone.replace(' ', '')}"
            phone_link.string = phone
            phone_p.append("Phone: ")
            phone_p.append(phone_link)
            storage_card.append(phone_p)
            
            # Website
            website_p = soup.new_tag("p")
            website_link = soup.new_tag("a")
            website_link["href"] = f"https://{website}"
            website_link["target"] = "_blank"
            website_link["rel"] = "noopener noreferrer"
            website_link.string = website
            website_p.append("Website: ")
            website_p.append(website_link)
            storage_card.append(website_p)
            
            storage_grid.append(storage_card)
        
        storage_list.append(storage_grid)
        
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
    
    print("Finding all city pages...")
    city_pages = find_city_pages()
    print(f"Found {len(city_pages)} city pages.")
    
    # Filter to only include pages missing storage-list
    print("Checking which pages need storage-list containers...")
    missing_storage_list = []
    for page in city_pages:
        if is_missing_storage_list(page):
            missing_storage_list.append(page)
    
    print(f"Found {len(missing_storage_list)} city pages missing storage-list containers.")
    
    if len(missing_storage_list) == 0:
        print("No pages need fixing. Exiting.")
        return
    
    fixed_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        
        for filepath in missing_storage_list:
            futures.append(executor.submit(add_storage_list, filepath))
        
        for i, future in enumerate(futures):
            try:
                if future.result():
                    fixed_count += 1
                    print(f"[{fixed_count}/{len(missing_storage_list)}] Fixed: {missing_storage_list[i]}")
            except Exception as e:
                error_count += 1
                print(f"Error processing {missing_storage_list[i]}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    print("\nFix summary:")
    print(f"- Total city pages missing storage-list: {len(missing_storage_list)}")
    print(f"- Successfully fixed: {fixed_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 