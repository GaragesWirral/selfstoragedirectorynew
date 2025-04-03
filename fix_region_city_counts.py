import os
import re
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

def find_regions_page():
    """Find the regions index.html file."""
    regions_file = os.path.join(os.getcwd(), "website", "selfstorageregions", "index.html")
    if os.path.exists(regions_file):
        return regions_file
    return None

def count_cities_in_region(region_dir):
    """Count the number of cities in a region."""
    try:
        # Count folders that start with 'selfstorage' (city folders)
        city_count = 0
        for item in os.listdir(region_dir):
            item_path = os.path.join(region_dir, item)
            if os.path.isdir(item_path) and item.startswith("selfstorage"):
                # Make sure it's a city folder and not something else
                index_file = os.path.join(item_path, "index.html")
                if os.path.exists(index_file):
                    city_count += 1
        
        return city_count
    except Exception as e:
        print(f"Error counting cities in {region_dir}: {str(e)}")
        return 0

def clean_name(name):
    """Clean a region or city name from a directory path."""
    if name.startswith('selfstorage'):
        name = name[len('selfstorage'):]
    
    # Replace hyphens with spaces and title case
    name = name.replace('-', ' ').title()
    
    return name

def fix_region_city_counts(regions_file):
    """Fix the city counts in region boxes on the regions page."""
    try:
        with open(regions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        website_dir = os.path.join(os.getcwd(), "website")
        
        # Find all region cards - the regions page is using city-card class
        region_cards = soup.find_all(class_="city-card")
        
        updates_made = 0
        
        for region_card in region_cards:
            # Get the link to the region page
            link = region_card.find('a')
            if not link or not link.has_attr('href'):
                continue
            
            href = link['href']
            
            # Skip external links
            if href.startswith('http'):
                continue
                
            # Extract region name and path from the href
            # Example: "../selfstoragebedfordshire/index.html"
            href_parts = href.split('/')
            region_folder = None
            for part in href_parts:
                if part.startswith('selfstorage'):
                    region_folder = part
                    break
            
            if not region_folder:
                continue
                
            region_path = os.path.join(website_dir, region_folder)
            region_name = clean_name(region_folder)
            
            # Find the paragraph element containing the count
            count_elem = region_card.find('p')
            if not count_elem:
                continue
            
            # Count the cities in the region
            city_count = count_cities_in_region(region_path)
            
            if city_count == 0:
                print(f"Warning: No cities found in {region_name}")
                continue
            
            # Update the count text
            city_text = "City" if city_count == 1 else "Cities"
            count_text = f"{city_count} {city_text}"
            
            # Check if the text already contains the city count
            current_text = count_elem.text.strip().lower()
            already_cities = 'city' in current_text or 'cities' in current_text
            
            if not already_cities:
                count_elem.string = count_text
                updates_made += 1
                print(f"Updated {region_name} to show {city_count} {city_text}")
        
        if updates_made > 0:
            # Write the updated HTML back to the file
            with open(regions_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return updates_made
        
        return 0
    
    except Exception as e:
        print(f"Error fixing region city counts: {str(e)}")
        return 0

def main():
    start_time = time.time()
    
    print("Finding regions page...")
    regions_file = find_regions_page()
    
    if not regions_file:
        print("Regions page not found. Exiting.")
        return
    
    print(f"Found regions page: {regions_file}")
    
    total_updates = fix_region_city_counts(regions_file)
    
    elapsed_time = time.time() - start_time
    
    print("\nUpdate summary:")
    print(f"- Region boxes updated: {total_updates}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 