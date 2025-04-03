import os
from bs4 import BeautifulSoup
import re

def find_placeholder_facilities():
    """Find city pages that contain example/placeholder storage facilities."""
    placeholder_cities = []
    placeholder_patterns = [
        "example.com", "example.org", "123-456-7890", "987-654-3210",
        "abc storage", "xyz storage", "123 main st", "456 oak ave"
    ]
    
    for root, dirs, files in os.walk("website"):
        for file in files:
            if file == "index.html" and "selfstorage" in root and "selfstorageregions" not in root:
                # Check if it's a city page (subdirectory of a region)
                parts = root.split(os.sep)
                if len(parts) >= 3:
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().lower()  # Convert to lowercase for case-insensitive matching
                        
                        has_placeholder = False
                        for pattern in placeholder_patterns:
                            if pattern in content:
                                has_placeholder = True
                                break
                        
                        if has_placeholder:
                            city_path = root
                            region_path = os.path.dirname(city_path)
                            region_name = os.path.basename(region_path).replace('selfstorage', '')
                            city_name = os.path.basename(city_path).replace('selfstorage', '')
                            
                            placeholder_cities.append((region_name, city_name, filepath))
                            print(f"Found placeholder in {region_name}/{city_name}")
                    
                    except Exception as e:
                        print(f"Error checking {filepath}: {e}")
    
    return placeholder_cities

def main():
    """Find city pages with placeholder facilities and suggest how to update them."""
    placeholder_cities = find_placeholder_facilities()
    
    print(f"\nFound {len(placeholder_cities)} city pages with placeholder facilities:")
    
    # Group by region for easier processing
    regions_with_placeholders = {}
    for region, city, filepath in placeholder_cities:
        if region not in regions_with_placeholders:
            regions_with_placeholders[region] = []
        regions_with_placeholders[region].append((city, filepath))
    
    # Print results by region
    for region, cities in sorted(regions_with_placeholders.items()):
        print(f"\n{region.title()} ({len(cities)} cities):")
        for city, _ in sorted(cities):
            print(f"  - {city.replace('-', ' ').title()}")
    
    # Generate command to update these cities
    regions_to_update = list(regions_with_placeholders.keys())
    if regions_to_update:
        print("\nTo update these cities, run:")
        regions_str = " ".join([region.title() for region in regions_to_update])
        print(f"python update_city_pages.py {regions_str}")

if __name__ == "__main__":
    main() 