import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import time

def normalize_name(name):
    """Normalize a name by converting to lowercase, removing special characters, and replacing spaces with hyphens."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    return name

def get_region_directory(region):
    """Find the correct directory name for a region."""
    if not region:
        return None
    
    normalized_region = normalize_name(region)
    
    # Special case handling
    if normalized_region == 'aberdeenshire':
        return 'selfstorageaberdeenshire'
    elif normalized_region == 'aberdeen-city':
        return 'selfstorageaberdeen-city'
    elif normalized_region == 'city-of-edinburgh' or normalized_region == 'edinburgh-city':
        return 'selfstoragecity-of-edinburgh'
    elif normalized_region == 'london':
        return 'selfstoragegreater-london'
    
    # General case - prepend 'selfstorage'
    return f'selfstorage{normalized_region}'

def get_city_directory(city):
    """Find the correct directory name for a city."""
    if not city:
        return None
    
    normalized_city = normalize_name(city)
    
    # Special case handling
    if normalized_city == 'saint-albans':
        return 'selfstoragest-albans'
    elif normalized_city == 'st-albans':
        return 'selfstoragest-albans'
    
    # General case - prepend 'selfstorage'
    return f'selfstorage{normalized_city}'

def update_city_page(region, city, facilities_data, dry_run=False):
    """Update a city page with facility data."""
    region_dir = get_region_directory(region)
    city_dir = get_city_directory(city)
    
    if not region_dir or not city_dir:
        return False, f"Invalid region or city: {region}, {city}"
    
    city_html_path = f'website/{region_dir}/{city_dir}/index.html'
    
    # Check if the directory exists
    if not os.path.exists(os.path.dirname(city_html_path)):
        return False, f"Directory does not exist: {os.path.dirname(city_html_path)}"
    
    # Check if the file exists
    if not os.path.exists(city_html_path):
        return False, f"HTML file does not exist: {city_html_path}"
    
    if dry_run:
        return True, f"Would update {city_html_path} with {len(facilities_data)} facilities"
    
    # Read the HTML file
    try:
        with open(city_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file {city_html_path}: {str(e)}"
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the storage-list div
    storage_list = soup.find('div', class_='storage-list')
    if not storage_list:
        return False, f"Storage list not found in {city_html_path}"
    
    # Clear existing storage cards
    storage_list.clear()
    
    # Process each facility
    for facility in facilities_data:
        # Extract facility data
        name = str(facility.get('Name of Self Storage', '')).strip()
        website = str(facility.get('Website', '')).strip().replace('https://', '').replace('http://', '')
        email = str(facility.get('Email / Contact', '')).strip()
        phone = str(facility.get('Telephone Number', '')).strip()
        address = str(facility.get('Location', '')).strip()
        
        # Skip if essential data is missing
        if not name or not address:
            continue
        
        # Create description
        description = f"{name} provides self storage solutions in {city}, {region}. Located at {address} with easy access and secure storage options."
        
        # Create a new storage card
        card = soup.new_tag('div', attrs={'class': 'storage-card'})
        
        # Add facility name
        name_tag = soup.new_tag('h3')
        name_tag.string = name
        card.append(name_tag)
        
        # Create storage info container
        info = soup.new_tag('div', attrs={'class': 'storage-info'})
        
        # Add address
        address_p = soup.new_tag('p')
        address_strong = soup.new_tag('strong')
        address_strong.string = 'Address: '
        address_p.append(address_strong)
        address_p.append(address)
        info.append(address_p)
        
        # Add description
        desc_p = soup.new_tag('p')
        desc_strong = soup.new_tag('strong')
        desc_strong.string = 'Description: '
        desc_p.append(desc_strong)
        desc_p.append(description)
        info.append(desc_p)
        
        # Add features
        features_list = soup.new_tag('div', attrs={'class': 'features-list'})
        
        # Add standard features
        features = ["Secure Facility", "24/7 Access"]
        for feature in features:
            feature_tag = soup.new_tag('span', attrs={'class': 'feature-tag'})
            feature_tag.string = feature
            features_list.append(feature_tag)
        
        info.append(features_list)
        
        # Add contact info
        contact = soup.new_tag('div', attrs={'class': 'contact-info'})
        
        # Add phone
        if phone and str(phone).lower() != 'nan':
            phone_p = soup.new_tag('p')
            phone_strong = soup.new_tag('strong')
            phone_strong.string = 'Phone: '
            phone_p.append(phone_strong)
            
            phone_link = soup.new_tag('a', href=f"tel:{str(phone).replace(' ', '')}")
            phone_link.string = str(phone)
            phone_p.append(phone_link)
            contact.append(phone_p)
        
        # Add website
        if website and str(website).lower() != 'nan':
            website_p = soup.new_tag('p')
            website_strong = soup.new_tag('strong')
            website_strong.string = 'Website: '
            website_p.append(website_strong)
            
            website_link = soup.new_tag('a', href=f"https://{website}", target="_blank")
            website_link.string = website
            website_p.append(website_link)
            contact.append(website_p)
        
        # Add email
        if email and str(email).lower() != 'nan':
            email_p = soup.new_tag('p')
            email_strong = soup.new_tag('strong')
            email_strong.string = 'Email: '
            email_p.append(email_strong)
            
            email_link = soup.new_tag('a', href=f"mailto:{email}")
            email_link.string = email
            email_p.append(email_link)
            contact.append(email_p)
        
        info.append(contact)
        card.append(info)
        storage_list.append(card)
    
    # Update the HTML file
    try:
        with open(city_html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    except Exception as e:
        return False, f"Error writing to file {city_html_path}: {str(e)}"
    
    return True, f"Successfully updated {city} page with {len(facilities_data)} facilities"

def update_region_page(region, cities_data, dry_run=False):
    """Update a region page with city facility counts."""
    region_dir = get_region_directory(region)
    
    if not region_dir:
        return False, f"Invalid region: {region}"
    
    region_html_path = f'website/{region_dir}/index.html'
    
    # Check if the file exists
    if not os.path.exists(region_html_path):
        return False, f"Region HTML file does not exist: {region_html_path}"
    
    if dry_run:
        return True, f"Would update {region_html_path} with {len(cities_data)} cities"
    
    # Read the HTML file
    try:
        with open(region_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file {region_html_path}: {str(e)}"
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all city cards
    city_cards = soup.find_all('div', class_='city-card')
    updated_cities = set()
    
    for city, count in cities_data.items():
        city_normalized = normalize_name(city)
        
        # Find the matching city card
        for card in city_cards:
            city_name = card.find('h3')
            if not city_name:
                continue
                
            card_city = normalize_name(city_name.text)
            
            if card_city == city_normalized:
                # Update the count
                p_tag = card.find('p')
                if p_tag:
                    facility_text = f"{count} Storage {'Facilities' if count != 1 else 'Facility'}"
                    p_tag.string = facility_text
                    updated_cities.add(city)
                break
    
    # Save the region page
    try:
        with open(region_html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    except Exception as e:
        return False, f"Error writing to file {region_html_path}: {str(e)}"
    
    return True, f"Updated region page with counts for {len(updated_cities)} cities"

def main(dry_run=False):
    """Main function to update all facilities."""
    start_time = time.time()
    
    # Path to the Excel file
    excel_file = 'self storage facilities uk.xlsx'
    
    # Read the Excel file
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return
    
    # Check if required columns exist
    required_columns = ['Name of Self Storage', 'CITY', 'Region', 'Location']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing required columns in Excel file: {', '.join(missing_columns)}")
        return
    
    # Organize data by region and city
    facilities_by_region_city = {}
    city_counts_by_region = {}
    
    for _, row in df.iterrows():
        city = str(row.get('CITY', '')).strip()
        region = str(row.get('Region', '')).strip()
        
        if not city or not region:
            continue
        
        # Initialize dictionaries if needed
        if region not in facilities_by_region_city:
            facilities_by_region_city[region] = {}
            city_counts_by_region[region] = {}
        
        if city not in facilities_by_region_city[region]:
            facilities_by_region_city[region][city] = []
            city_counts_by_region[region][city] = 0
        
        # Add facility to the list
        facilities_by_region_city[region][city].append(row.to_dict())
        city_counts_by_region[region][city] += 1
    
    # Process each region and city
    success_count = 0
    error_count = 0
    errors = []
    
    # First do a dry run to check what pages we can update
    if dry_run:
        print("Performing dry run to check what pages we can update...")
        for region, cities in facilities_by_region_city.items():
            print(f"\nRegion: {region}")
            for city, facilities in cities.items():
                success, message = update_city_page(region, city, facilities, dry_run=True)
                if success:
                    print(f"  ✓ {city}: {message}")
                else:
                    print(f"  ✗ {city}: {message}")
        return
    
    # Update city pages
    for region, cities in facilities_by_region_city.items():
        print(f"\nProcessing region: {region}")
        
        for city, facilities in cities.items():
            success, message = update_city_page(region, city, facilities)
            
            if success:
                success_count += 1
                print(f"  ✓ {city}: {message}")
            else:
                error_count += 1
                errors.append(f"{region}/{city}: {message}")
                print(f"  ✗ {city}: {message}")
        
        # Update region page with city counts
        success, message = update_region_page(region, city_counts_by_region[region])
        
        if success:
            print(f"  ✓ Region page: {message}")
        else:
            errors.append(f"{region}: {message}")
            print(f"  ✗ Region page: {message}")
    
    # Print summary
    elapsed_time = time.time() - start_time
    print("\n" + "="*50)
    print(f"Update completed in {elapsed_time:.2f} seconds")
    print(f"Cities successfully updated: {success_count}")
    print(f"Errors encountered: {error_count}")
    
    if errors:
        print("\nErrors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

if __name__ == "__main__":
    # Set to True to do a dry run (check what can be updated without making changes)
    main(dry_run=False) 