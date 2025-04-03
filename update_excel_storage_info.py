import os
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import glob

def parse_excel_data(excel_file):
    """Parse the data from the Excel file."""
    facilities_by_city = {}
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Process each row
        for _, row in df.iterrows():
            try:
                # Extract city and region
                city = str(row.get('CITY', '')).strip()
                region = str(row.get('Region', '')).strip()
                
                if not city or not region:
                    continue
                    
                # Normalize region and city names
                region_key = region.lower().replace(' ', '')
                city_key = city.lower().replace(' ', '')
                
                # Create nested dictionary structure
                if region_key not in facilities_by_city:
                    facilities_by_city[region_key] = {}
                
                if city_key not in facilities_by_city[region_key]:
                    facilities_by_city[region_key][city_key] = []
                
                # Parse facility data
                name = str(row.get('Name of Self Storage', '')).strip()
                website = str(row.get('Website', '')).strip().replace('https://', '').replace('http://', '')
                email = str(row.get('Email / Contact', '')).strip()
                phone = str(row.get('Telephone Number', '')).strip()
                address = str(row.get('Location', '')).strip()
                
                # Skip if essential data is missing
                if not name or not address:
                    continue
                
                # Create a description based on facility data
                description = f"{name} provides self storage solutions in {city}, {region}. Located at {address} with easy access and secure storage options."
                
                # Add some default features
                features = ["Secure Facility", "24/7 Access"]
                
                facility = {
                    'name': name,
                    'address': address,
                    'phone': phone,
                    'website': website,
                    'email': email,
                    'description': description,
                    'features': features
                }
                
                facilities_by_city[region_key][city_key].append(facility)
                
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
        
        return facilities_by_city
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return {}

def find_all_region_directories():
    """Find all region directories in the website folder."""
    all_dirs = glob.glob("website/selfstorage*/")
    region_dirs = {}
    
    for dir_path in all_dirs:
        # Extract the region name from the path
        region_name = os.path.basename(os.path.dirname(dir_path))
        if region_name.startswith('selfstorage'):
            region_key = region_name.replace('selfstorage', '').lower()
            region_dirs[region_key] = region_name.replace('selfstorage', '')
    
    return region_dirs

def find_all_city_directories():
    """Find all city directories for each region."""
    city_dirs = {}
    all_region_dirs = glob.glob("website/selfstorage*/")
    
    for region_dir in all_region_dirs:
        region_name = os.path.basename(os.path.dirname(region_dir))
        region_key = region_name.replace('selfstorage', '').lower()
        
        city_dirs[region_key] = {}
        all_city_dirs = glob.glob(f"{region_dir}selfstorage*/")
        
        for city_dir in all_city_dirs:
            city_name = os.path.basename(os.path.dirname(city_dir))
            if city_name.startswith('selfstorage'):
                city_key = city_name.replace('selfstorage', '').lower()
                city_dirs[region_key][city_key] = city_name.replace('selfstorage', '')
    
    return city_dirs

def get_region_directory(region, all_region_dirs):
    """Get the correct directory name for a region."""
    # Normalize the region name
    region_key = region.lower().replace(' ', '').replace('-', '').replace('&', 'and')
    
    # Direct match
    if region_key in all_region_dirs:
        return all_region_dirs[region_key]
    
    # Handle special cases and variations
    special_cases = {
        'cityofedinburgh': 'city-of-edinburgh',
        'greaterlondon': 'greater-london',
        'westyorkshire': 'west-yorkshire',
        'southyorkshire': 'south-yorkshire',
        'westmidlands': 'west-midlands',
        'eastmidlands': 'east-midlands',
        'northyorkshire': 'north-yorkshire',
        'cityofaberdeen': 'aberdeenshire', 
        'aberdeencity': 'aberdeenshire',
        'argyllandbute': 'argyll-and-bute',
        'dumfriesandgalloway': 'dumfries-and-galloway',
        'dundeecity': 'dundee',
        'eastayrshire': 'east-ayrshire',
        'eastdunbartonshire': 'east-dunbartonshire',
        'eastlothian': 'east-lothian',
        'eastrenfrewshire': 'east-renfrewshire',
        'eileansiar': 'eilean-siar',
        'northayrshire': 'north-ayrshire',
        'northlanarkshire': 'north-lanarkshire',
        'perthandkinross': 'perth-and-kinross',
        'scottishborders': 'scottish-borders',
        'shetlandislands': 'shetland-islands',
        'southayrshire': 'south-ayrshire',
        'southlanarkshire': 'south-lanarkshire',
        'westdunbartonshire': 'west-dunbartonshire',
        'westlothian': 'west-lothian'
    }
    
    # Check special cases
    if region_key in special_cases:
        special_key = special_cases[region_key]
        for existing_key, dir_name in all_region_dirs.items():
            if special_key == existing_key or special_key.replace('-', '') == existing_key:
                return dir_name
    
    # Try with various transformations
    variations = [
        region_key,
        region_key.replace('shire', ''),
        region_key.replace('and', ''),
        region_key + 'shire'
    ]
    
    for var in variations:
        for existing_key, dir_name in all_region_dirs.items():
            if var == existing_key or var in existing_key or existing_key in var:
                return dir_name
    
    # For debugging
    print(f"Could not find directory for region: {region}")
    return None

def get_city_directory(city, region_key, all_city_dirs):
    """Get the correct directory name for a city in a region."""
    # Clean and normalize city name
    city_clean = city.lower()
    city_clean = re.sub(r'[,‎].*$', '', city_clean)  # Remove anything after a comma
    city_clean = city_clean.replace(' ', '').replace('-', '').replace('&', 'and')
    
    # Check if the region exists in our directory map
    if region_key not in all_city_dirs:
        return None
    
    # Direct match
    if city_clean in all_city_dirs[region_key]:
        return all_city_dirs[region_key][city_clean]
    
    # Try with variations
    for existing_key, dir_name in all_city_dirs[region_key].items():
        if city_clean == existing_key or city_clean.startswith(existing_key) or existing_key.startswith(city_clean):
            return dir_name
    
    # For debugging
    print(f"Could not find directory for city: {city} in region: {region_key}")
    return None

def update_city_page(city, region, region_dir_name, city_dir_name, facilities_data):
    """Update a city page with the correct storage facilities."""
    region_dir = f"website/selfstorage{region_dir_name}"
    city_dir = f"{region_dir}/selfstorage{city_dir_name}"
    city_index = f"{city_dir}/index.html"
    
    if not os.path.exists(city_index):
        print(f"City page not found: {city_index}")
        return False
    
    try:
        with open(city_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the storage-list div
        storage_list = soup.find('div', class_='storage-list')
        if not storage_list:
            print(f"Storage list not found in {city_index}")
            return False
        
        # Clear existing storage cards
        storage_list.clear()
        
        # Add new storage cards based on Excel data
        for facility in facilities_data:
            card = soup.new_tag('div', attrs={'class': 'storage-card'})
            
            # Add facility name
            name = soup.new_tag('h3')
            name.string = facility['name']
            card.append(name)
            
            # Create storage info container
            info = soup.new_tag('div', attrs={'class': 'storage-info'})
            
            # Add address
            address = soup.new_tag('p')
            address_strong = soup.new_tag('strong')
            address_strong.string = 'Address: '
            address.append(address_strong)
            address.append(facility['address'])
            info.append(address)
            
            # Add description
            desc = soup.new_tag('p')
            desc_strong = soup.new_tag('strong')
            desc_strong.string = 'Description: '
            desc.append(desc_strong)
            desc.append(facility['description'])
            info.append(desc)
            
            # Add features
            features_list = soup.new_tag('div', attrs={'class': 'features-list'})
            for feature in facility['features']:
                if feature:  # Skip empty features
                    feature_tag = soup.new_tag('span', attrs={'class': 'feature-tag'})
                    feature_tag.string = feature
                    features_list.append(feature_tag)
            info.append(features_list)
            
            # Add contact info
            contact = soup.new_tag('div', attrs={'class': 'contact-info'})
            
            # Add phone
            if facility['phone']:
                phone = soup.new_tag('p')
                phone_strong = soup.new_tag('strong')
                phone_strong.string = 'Phone: '
                phone.append(phone_strong)
                
                phone_link = soup.new_tag('a', href=f"tel:{facility['phone'].replace(' ', '')}")
                phone_link.string = facility['phone']
                phone.append(phone_link)
                contact.append(phone)
            
            # Add website
            if facility['website']:
                website = soup.new_tag('p')
                website_strong = soup.new_tag('strong')
                website_strong.string = 'Website: '
                website.append(website_strong)
                
                website_link = soup.new_tag('a', href=f"https://{facility['website']}", target="_blank")
                website_link.string = facility['website']
                website.append(website_link)
                contact.append(website)
            
            # Add email if available
            if facility['email']:
                email = soup.new_tag('p')
                email_strong = soup.new_tag('strong')
                email_strong.string = 'Email: '
                email.append(email_strong)
                
                email_link = soup.new_tag('a', href=f"mailto:{facility['email']}")
                email_link.string = facility['email']
                email.append(email_link)
                contact.append(email)
            
            info.append(contact)
            card.append(info)
            storage_list.append(card)
        
        # Update the HTML file
        with open(city_index, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Successfully updated {city_index} with {len(facilities_data)} facilities")
        return True
    except Exception as e:
        print(f"Error updating {city_index}: {e}")
        return False

def update_region_page(region, region_dir_name, cities_facilities):
    """Update the region page with the correct count of storage facilities per city."""
    region_dir = f"website/selfstorage{region_dir_name}"
    region_index = f"{region_dir}/index.html"
    
    if not os.path.exists(region_index):
        print(f"Region page not found: {region_index}")
        return False
    
    try:
        with open(region_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all city cards
        city_cards = soup.find_all('div', class_='city-card')
        updated_count = 0
        
        for card in city_cards:
            city_name = card.find('h3').text.lower().replace(' ', '').replace('-', '')
            
            # Normalize Excel city names
            normalized_cities = {}
            for excel_city, facilities in cities_facilities.items():
                # Clean and normalize city name from Excel
                clean_name = excel_city.lower()
                clean_name = re.sub(r'[,‎].*$', '', clean_name)  # Remove anything after a comma 
                clean_name = clean_name.replace(' ', '').replace('-', '')
                normalized_cities[clean_name] = (excel_city, facilities)
            
            # Try to match city name
            matched_city = None
            matched_facilities = []
            
            for norm_name, (orig_name, facilities) in normalized_cities.items():
                if city_name == norm_name or city_name.startswith(norm_name) or norm_name.startswith(city_name):
                    matched_city = orig_name
                    matched_facilities = facilities
                    break
            
            if matched_city:
                facilities_count = len(matched_facilities)
                facility_text = f"{facilities_count} Storage {'Facilities' if facilities_count != 1 else 'Facility'}"
                
                # Update the count text
                p_tag = card.find('p')
                if p_tag:
                    if p_tag.text != facility_text:
                        p_tag.string = facility_text
                        print(f"Updated card for {matched_city} with '{facility_text}'")
                        updated_count += 1
        
        # Update the HTML file
        with open(region_index, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Updated {updated_count} city cards in {region_dir_name}")
        return True
    except Exception as e:
        print(f"Error updating {region_index}: {e}")
        return False

def main():
    """Main function to update all pages."""
    start_time = time.time()
    
    # Excel file path
    excel_file = 'self storage facilities uk.xlsx'
    
    # Find all region and city directories
    print("Mapping website directory structure...")
    all_region_dirs = find_all_region_directories()
    all_city_dirs = find_all_city_directories()
    
    # Parse the Excel data
    print("Parsing Excel data...")
    facilities_data = parse_excel_data(excel_file)
    
    if not facilities_data:
        print("No data found or error reading the Excel file.")
        return
        
    total_updated = 0
    errors = 0
    
    # Process one region at a time to handle errors better
    for region, cities in facilities_data.items():
        print(f"\nProcessing region: {region}")
        
        # Find the region directory
        region_dir_name = get_region_directory(region, all_region_dirs)
        if not region_dir_name:
            print(f"Could not find directory for region: {region}")
            continue
            
        # Update the region page
        update_region_page(region, region_dir_name, cities)
        
        # Update each city page
        for city, facilities in cities.items():
            print(f"  Processing city: {city}")
            
            # Find the city directory
            city_dir_name = get_city_directory(city, region_dir_name.lower(), all_city_dirs)
            if not city_dir_name:
                print(f"Could not find directory for city: {city} in region: {region}")
                errors += 1
                continue
                
            if update_city_page(city, region, region_dir_name, city_dir_name, facilities):
                total_updated += 1
            else:
                errors += 1
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    print(f"\nResults summary:")
    print(f"- Total cities updated: {total_updated}")
    print(f"- Errors: {errors}")
    print(f"- Time taken: {time_taken:.2f} seconds")

if __name__ == "__main__":
    main() 