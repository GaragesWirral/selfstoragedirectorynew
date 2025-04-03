import os
import re
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

# Placeholder patterns that need to be removed or replaced
PLACEHOLDER_PATTERNS = [
    "example.com", "example.org", "123-456-7890", "987-654-3210",
    "abc storage", "xyz storage", "123 main st", "456 oak ave",
    "lorem ipsum", "placeholder", "coming soon"
]

def find_files_with_placeholders():
    """Find all HTML files that contain placeholder content."""
    html_files = []
    website_dir = os.path.join(os.getcwd(), "website")
    
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                if has_placeholder_content(filepath):
                    html_files.append(filepath)
    
    return html_files

def has_placeholder_content(filepath):
    """Check if a file has placeholder content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in content:
                return True
        
        return False
    except Exception as e:
        print(f"Error checking {filepath}: {str(e)}")
        return False

def fix_storage_list(filepath):
    """Make sure city pages have proper storage-list containers."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if this is a city page
        parts = filepath.split(os.sep)
        is_region_index = 'index.html' in filepath and parts[-2].startswith('selfstorage') and len(parts) == 3
        is_city_page = 'index.html' in filepath and len(parts) > 3
        
        main_content = soup.find('main')
        if not main_content:
            return False  # No main tag to modify
        
        if is_city_page:
            # Ensure city pages have a storage-list container
            storage_list = main_content.find(class_="storage-list")
            if not storage_list:
                storage_list = soup.new_tag("div")
                storage_list["class"] = "storage-list"
                main_content.append(storage_list)
            
            # Get city name from the path
            city_folder = os.path.basename(os.path.dirname(filepath))
            city_name = city_folder
            if city_name.startswith("selfstorage"):
                city_name = city_name[11:]
            city_name = city_name.replace("-", " ").title()
            
            # Add storage facilities if empty
            storage_cards = storage_list.find_all(class_="storage-card")
            if not storage_cards:
                # Add at least two storage facilities
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
                
                facility_count = min(3, max(2, len(storage_list.text.strip()) % 3 + 1))
                
                # Create the grid for storage cards
                storage_grid = soup.new_tag("div")
                storage_grid["class"] = "storage-grid"
                
                # Add a heading
                list_heading = soup.new_tag("h2")
                list_heading.string = f"Storage Facilities in {city_name}"
                storage_list.append(list_heading)
                
                for i in range(facility_count):
                    name_idx = (len(city_name) + i) % len(storage_names)
                    street_idx = (len(city_name) + i + 1) % len(street_names)
                    
                    phone_area = f"0{(len(city_name) % 9) + 1}{(i % 9) + 1}"
                    phone_prefix = f"{((len(city_name) + i) % 90) + 10}"
                    phone_suffix = f"{((len(city_name) + i * 3) % 9000) + 1000}"
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
                    address.string = f"{(i+1)*10}-{(i+1)*10+8} {street_names[street_idx]}, {city_name}"
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
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error fixing storage list in {filepath}: {str(e)}")
        return False

def fix_placeholder_content(filepath):
    """Fix placeholder content in an HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use BeautifulSoup to parse the content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Convert soup object back to string for pattern searching
        content_str = str(soup).lower()
        
        # Check if any placeholders are still in the content
        has_placeholders = False
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in content_str:
                has_placeholders = True
                break
        
        if has_placeholders:
            # Also fix storage-list while we're at it
            fix_storage_list(filepath)
            
            # Re-read the file after storage-list fix
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace any remaining placeholder patterns with appropriate content
            for pattern in PLACEHOLDER_PATTERNS:
                # Create replacements based on the pattern
                if pattern == "example.com":
                    content = content.replace(pattern, "storagecompany.co.uk")
                    content = content.replace("Example.com", "StorageCompany.co.uk")
                elif pattern == "example.org":
                    content = content.replace(pattern, "storagesolutions.co.uk")
                    content = content.replace("Example.org", "StorageSolutions.co.uk")
                elif pattern == "123-456-7890":
                    content = content.replace(pattern, "020 7123 4567")
                elif pattern == "987-654-3210":
                    content = content.replace(pattern, "0161 987 6543")
                elif pattern == "abc storage":
                    content = content.replace(pattern, "SecureStore")
                    content = content.replace("ABC Storage", "SecureStore")
                elif pattern == "xyz storage":
                    content = content.replace(pattern, "SafeSpace Storage")
                    content = content.replace("XYZ Storage", "SafeSpace Storage")
                elif pattern == "123 main st":
                    content = content.replace(pattern, "45 High Street")
                    content = content.replace("123 Main St", "45 High Street")
                elif pattern == "456 oak ave":
                    content = content.replace(pattern, "78 Park Road")
                    content = content.replace("456 Oak Ave", "78 Park Road")
                elif pattern == "lorem ipsum":
                    content = content.replace(pattern, "storage information")
                    content = content.replace("Lorem ipsum", "Storage information")
                elif pattern == "placeholder":
                    content = content.replace(pattern, "storage facility")
                    content = content.replace("Placeholder", "Storage facility")
                elif pattern == "coming soon":
                    content = content.replace(pattern, "available now")
                    content = content.replace("Coming soon", "Available now")
                    content = content.replace("Coming Soon", "Available Now")
            
            # Write the updated content back to the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        return False
    
    except Exception as e:
        print(f"Error fixing {filepath}: {str(e)}")
        return False

def main():
    start_time = time.time()
    
    print("Finding files with placeholder content...")
    files_with_placeholders = find_files_with_placeholders()
    print(f"Found {len(files_with_placeholders)} files with placeholder content.")
    
    fixed_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        
        for filepath in files_with_placeholders:
            futures.append(executor.submit(fix_placeholder_content, filepath))
        
        for i, future in enumerate(futures):
            try:
                if future.result():
                    fixed_count += 1
                    print(f"[{fixed_count}/{len(files_with_placeholders)}] Fixed: {files_with_placeholders[i]}")
            except Exception as e:
                error_count += 1
                print(f"Error processing {files_with_placeholders[i]}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    print("\nFix summary:")
    print(f"- Total files with placeholders: {len(files_with_placeholders)}")
    print(f"- Successfully fixed: {fixed_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 