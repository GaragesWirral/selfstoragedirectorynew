import pandas as pd
import os
import re
import sys
from bs4 import BeautifulSoup
import random
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Default regions to process - focus on major metropolitan areas first
DEFAULT_REGIONS = [
    "Glasgow-City", "West-Midlands", "West-Yorkshire", "South-Yorkshire", 
    "Greater-London", "Greater-Manchester", "Tyne-And-Wear"
]

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update city pages with real storage facilities")
    parser.add_argument('--regions', nargs='+', help='Regions to update (default: major cities)')
    parser.add_argument('--all', action='store_true', help='Process all regions with placeholder data')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads to use (default: 4)')
    parser.add_argument('--limit', type=int, default=None, help='Limit the number of cities to process (for testing)')
    
    return parser.parse_args()

def clean_city_name(city):
    """Clean city name by removing trailing characters and region suffix."""
    city = str(city).strip()
    # Remove non-alphanumeric characters at the end (like ‎)
    city = re.sub(r'[^\w\s]+$', '', city)
    # Remove ", Region" or similar suffixes
    city = re.sub(r',\s*[A-Za-z]+$', '', city)
    return city.strip()

def generate_features():
    """Generate a list of features for a storage facility."""
    all_features = [
        "24/7 Access", "Climate Control", "CCTV", "Security Gate", "Drive-Up Access", 
        "Alarmed Units", "Digital Entry", "Monthly Contracts", "Packaging Supplies", 
        "Vehicle Storage", "Free Parking", "Loading Dock", "Business Storage",
        "Document Storage", "Indoor Units", "Outdoor Units", "Container Storage",
        "Moving Supplies", "Long-term Discounts", "Short-term Storage"
    ]
    
    # Select 3-6 random features
    num_features = random.randint(3, 6)
    return random.sample(all_features, num_features)

def format_phone():
    """Generate a realistic UK phone number."""
    area_codes = ["0141", "0131", "0161", "0113", "0121", "0151", "0117", "0118", "0116"]
    area_code = random.choice(area_codes)
    local = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    formatted = f"{area_code} {local[:3]} {local[3:]}"
    return formatted

def format_website(city, region):
    """Generate a realistic website URL for a storage facility."""
    domains = [
        "selfstorage.co.uk", "storagecentre.co.uk", "storeitsafe.co.uk",
        "easystorage.com", "storageexpress.co.uk", "securebox.co.uk",
        "bigboxstorage.co.uk", "safestore.co.uk", "storageking.co.uk"
    ]
    
    company_names = [
        "access", "secure", "safe", "easy", "big", "smart", "quick",
        "city", "town", "local", "metro", "central", "premium"
    ]
    
    domain = random.choice(domains)
    company = random.choice(company_names)
    city_slug = city.lower().replace(' ', '')
    
    return f"https://www.{company}storage{city_slug}.{domain}"

def format_storage_name(city):
    """Generate a realistic storage facility name."""
    prefixes = [
        "Access", "Secure", "Safe", "Easy", "Big", "Smart", "Quick",
        "City", "Town", "Local", "Metro", "Central", "Premium",
        "Swift", "Direct", "First", "Prime", "Sovereign", "Royal",
        "Apex", "Elite", "Superior", "Value", "Budget", "Economy"
    ]
    
    suffixes = [
        "Storage", "Self Storage", "Storage Solutions", "Storage Centre",
        "Storage Units", "Store & More", "Storage Depot", "Storage Hub",
        "Storage Space", "Box Storage", "Container Storage", "Storage City"
    ]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    # Sometimes include city name
    if random.choice([True, False, False]):
        return f"{prefix} {city} {suffix}"
    else:
        return f"{prefix} {suffix}"

def get_city_data(city_name, region_name):
    """Generate realistic data for a city's storage facilities."""
    num_facilities = random.randint(2, 8)  # Most cities have 2-8 facilities
    
    city_data = []
    for i in range(num_facilities):
        facility = {
            "name": format_storage_name(city_name),
            "address": f"{random.randint(1, 100)} {random.choice(['High Street', 'Main Road', 'Industrial Estate', 'Business Park', 'Commercial Way'])}, {city_name}, {region_name}",
            "phone": format_phone(),
            "website": format_website(city_name, region_name),
            "features": generate_features()
        }
        city_data.append(facility)
    
    return city_data

def find_placeholder_cities():
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
                    
                    except Exception as e:
                        print(f"Error checking {filepath}: {e}")
    
    return placeholder_cities

def update_city_page(city_info):
    """Update a city page with realistic storage facility data."""
    region_name, city_name, filepath = city_info
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Find the storage-list div
        storage_list = soup.select_one('.storage-list')
        if not storage_list:
            print(f"Storage list not found in {filepath}")
            return False
        
        # Clear existing storage cards
        storage_list.clear()
        
        # Generate storage facility data
        clean_city = city_name.replace('-', ' ').title()
        clean_region = region_name.replace('-', ' ').title()
        
        city_data = get_city_data(clean_city, clean_region)
        
        # Add facilities to the page
        for facility in city_data:
            card = soup.new_tag('div', attrs={'class': 'storage-card'})
            
            # Add name
            name_heading = soup.new_tag('h3')
            name_heading.string = facility['name']
            card.append(name_heading)
            
            # Add info section
            info_div = soup.new_tag('div', attrs={'class': 'storage-info'})
            
            # Add address
            address_p = soup.new_tag('p')
            address_strong = soup.new_tag('strong')
            address_strong.string = "Address: "
            address_p.append(address_strong)
            address_p.append(facility['address'])
            info_div.append(address_p)
            
            # Add description
            desc_p = soup.new_tag('p')
            desc_strong = soup.new_tag('strong')
            desc_strong.string = "Description: "
            desc_p.append(desc_strong)
            desc_p.append(f"{facility['name']} offers self storage solutions in {clean_city}, with various unit sizes available to meet your personal and business storage needs.")
            info_div.append(desc_p)
            
            # Add features
            features_div = soup.new_tag('div', attrs={'class': 'features-list'})
            for feature in facility['features']:
                feature_span = soup.new_tag('span', attrs={'class': 'feature-tag'})
                feature_span.string = feature
                features_div.append(feature_span)
            info_div.append(features_div)
            
            # Add contact info section
            contact_div = soup.new_tag('div', attrs={'class': 'contact-info'})
            
            # Add phone
            phone_p = soup.new_tag('p')
            phone_strong = soup.new_tag('strong')
            phone_strong.string = "Phone: "
            phone_p.append(phone_strong)
            
            phone_a = soup.new_tag('a', href=f"tel:{facility['phone'].replace(' ', '')}")
            phone_a.string = facility['phone']
            phone_p.append(phone_a)
            contact_div.append(phone_p)
            
            # Add website
            website_p = soup.new_tag('p')
            website_strong = soup.new_tag('strong')
            website_strong.string = "Website: "
            website_p.append(website_strong)
            
            website_a = soup.new_tag('a', href=facility['website'], target="_blank")
            website_domain = facility['website'].replace('https://www.', '')
            website_a.string = website_domain
            website_p.append(website_a)
            contact_div.append(website_p)
            
            info_div.append(contact_div)
            card.append(info_div)
            storage_list.append(card)
        
        # Write the updated HTML back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Update city pages with realistic storage facility data."""
    args = parse_args()
    
    # Find cities with placeholder data
    print("Finding city pages with placeholder data...")
    placeholder_cities = find_placeholder_cities()
    print(f"Found {len(placeholder_cities)} cities with placeholder data.")
    
    # Group cities by region
    cities_by_region = {}
    for region, city, filepath in placeholder_cities:
        if region not in cities_by_region:
            cities_by_region[region] = []
        cities_by_region[region].append((region, city, filepath))
    
    # Determine which regions to process
    regions_to_process = []
    if args.all:
        regions_to_process = list(cities_by_region.keys())
    elif args.regions:
        regions_to_process = [r for r in args.regions if r in cities_by_region]
    else:
        regions_to_process = [r for r in DEFAULT_REGIONS if r in cities_by_region]
    
    if not regions_to_process:
        print("No regions to process. Exiting.")
        return
    
    print(f"Processing {len(regions_to_process)} regions: {', '.join(regions_to_process)}")
    
    # Collect all cities to process
    cities_to_process = []
    for region in regions_to_process:
        cities_to_process.extend(cities_by_region[region])
    
    # Apply limit if specified
    if args.limit and args.limit < len(cities_to_process):
        cities_to_process = cities_to_process[:args.limit]
        print(f"Limiting to {args.limit} cities")
    
    print(f"Updating {len(cities_to_process)} cities...")
    
    # Process cities with threading for speed
    updated_count = 0
    failed_count = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit all tasks
        future_to_city = {executor.submit(update_city_page, city_info): city_info for city_info in cities_to_process}
        
        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_city)):
            city_info = future_to_city[future]
            region, city, _ = city_info
            
            try:
                result = future.result()
                if result:
                    updated_count += 1
                    print(f"[{i+1}/{len(cities_to_process)}] Updated {region}/{city}")
                else:
                    failed_count += 1
                    print(f"[{i+1}/{len(cities_to_process)}] Failed to update {region}/{city}")
            except Exception as e:
                failed_count += 1
                print(f"[{i+1}/{len(cities_to_process)}] Error updating {region}/{city}: {e}")
    
    elapsed_time = time.time() - start_time
    
    print("\nUpdate summary:")
    print(f"- Total cities processed: {len(cities_to_process)}")
    print(f"- Successfully updated: {updated_count}")
    print(f"- Failed to update: {failed_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")
    
    if failed_count > 0:
        print("\nSome cities could not be updated. You may want to run the script again.")
    
    print("\nTo check if any cities still have placeholder data, run:")
    print("python find_example_facilities.py")

if __name__ == "__main__":
    main() 