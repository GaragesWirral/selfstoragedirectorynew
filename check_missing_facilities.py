import os
from bs4 import BeautifulSoup

def find_problematic_city_pages():
    """Find all city HTML pages that have issues with storage facilities."""
    problematic_cities = []
    regions_with_issues = {}
    placeholder_content = set([
        "no storage facilities found",
        "coming soon",
        "no facilities available"
    ])
    
    for root, dirs, files in os.walk("website"):
        for file in files:
            if file == "index.html" and "selfstorage" in root and "selfstorageregions" not in root:
                # Check if it's a city page (subdirectory of a region)
                parts = root.split(os.sep)
                if len(parts) >= 3:
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            soup = BeautifulSoup(content, 'html.parser')
                        
                        city_path = root
                        region_path = os.path.dirname(city_path)
                        region_name = os.path.basename(region_path).replace('selfstorage', '')
                        city_name = os.path.basename(city_path).replace('selfstorage', '')
                        issue = None
                        
                        # Check if this page has the basic storage structure
                        storage_list = soup.select_one('.storage-list')
                        if not storage_list:
                            issue = "Missing storage-list structure"
                        else:
                            # Check if storage cards exist
                            storage_cards = storage_list.select('.storage-card')
                            if not storage_cards:
                                issue = "No storage cards found in storage-list"
                            else:
                                # Check for exact placeholder content phrases
                                for card in storage_cards:
                                    text = card.get_text().strip().lower()
                                    is_placeholder = False
                                    
                                    for placeholder in placeholder_content:
                                        if placeholder.lower() in text:
                                            is_placeholder = True
                                            break
                                    
                                    # Check for empty cards
                                    if len(card.get_text().strip()) < 10:
                                        is_placeholder = True
                                    
                                    if is_placeholder:
                                        issue = "Contains placeholder content"
                                        break
                        
                        if issue:
                            problematic_cities.append((region_name, city_name, filepath, issue))
                            
                            # Add to regions dict
                            if region_name not in regions_with_issues:
                                regions_with_issues[region_name] = []
                            regions_with_issues[region_name].append((city_name, issue))
                    
                    except Exception as e:
                        print(f"Error checking {filepath}: {e}")
                        problematic_cities.append((region_name, city_name, filepath, str(e)))
                        
                        # Add to regions dict
                        if region_name not in regions_with_issues:
                            regions_with_issues[region_name] = []
                        regions_with_issues[region_name].append((city_name, str(e)))
    
    return problematic_cities, regions_with_issues

def main():
    """Main function to find and report problematic city pages."""
    problematic_cities, regions_with_issues = find_problematic_city_pages()
    
    print(f"Found {len(problematic_cities)} city pages with potential issues")
    
    # Print regions with problematic cities
    print("\nRegions with problematic city pages:")
    for region, cities in sorted(regions_with_issues.items()):
        print(f"\n{region.title()} ({len(cities)} cities):")
        for city, issue in sorted(cities):
            print(f"  - {city.replace('-', ' ').title()}: {issue}")
    
    # Print recommendations
    print("\nRecommended next steps:")
    print("1. Run update_city_pages.py for these specific regions to add storage facility data")
    print("2. Check if the city HTML structure is correct - they may need the storage-list class")
    print("3. Check if Excel data source has entries for these cities")

if __name__ == "__main__":
    main() 