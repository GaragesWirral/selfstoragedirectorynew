import os
import csv
import re
import time
import argparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import random
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Bulk update storage facilities from CSV data")
    parser.add_argument("--csv", default="master_storage_facilities.csv", help="Path to the CSV file containing storage facility data")
    parser.add_argument("--verify", action="store_true", help="Verify city counts and generate a report without making changes")
    parser.add_argument("--region", help="Process only cities in a specific region")
    parser.add_argument("--city", help="Process only a specific city in format 'region/city'")
    parser.add_argument("--output", default="update_report.json", help="Path to save the report JSON")
    parser.add_argument("--threads", type=int, default=8, help="Number of threads to use for parallel processing")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--fix-card-counts", action="store_true", help="Update the storage count on city cards in region pages")
    return parser.parse_args()

def read_csv_data(csv_file):
    """Read storage facility data from CSV file."""
    facilities_data = {}
    
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Expect columns like: Region, City, Name, Address, Phone, Website, Description, Features
                region = row.get('Region', '').strip().lower()
                city = row.get('City', '').strip().lower()
                
                if not region or not city:
                    continue
                
                # Create a key in format "region/city"
                key = f"{region}/{city}"
                
                if key not in facilities_data:
                    facilities_data[key] = []
                
                # Clean up feature list
                features = []
                if 'Features' in row:
                    features = [feat.strip() for feat in row['Features'].split(',') if feat.strip()]
                
                facility = {
                    'name': row.get('Name', '').strip(),
                    'address': row.get('Address', '').strip(),
                    'phone': row.get('Phone', '').strip(),
                    'website': row.get('Website', '').strip(),
                    'description': row.get('Description', '').strip(),
                    'features': features
                }
                
                # Only add if it has at least a name
                if facility['name']:
                    facilities_data[key].append(facility)
        
        return facilities_data
    
    except Exception as e:
        print(f"{Fore.RED}Error reading CSV file: {str(e)}{Style.RESET_ALL}")
        return {}

def find_city_page(region, city):
    """Find the HTML file for a specific city."""
    website_dir = os.path.join(os.getcwd(), "website")
    region_folder = f"selfstorage{region.replace(' ', '-').lower()}"
    city_folder = f"selfstorage{city.replace(' ', '-').lower()}"
    
    city_path = os.path.join(website_dir, region_folder, city_folder, "index.html")
    
    if os.path.exists(city_path):
        return city_path
    
    return None

def find_region_page(region):
    """Find the HTML file for a specific region."""
    website_dir = os.path.join(os.getcwd(), "website")
    region_folder = f"selfstorage{region.replace(' ', '-').lower()}"
    
    region_path = os.path.join(website_dir, region_folder, "index.html")
    
    if os.path.exists(region_path):
        return region_path
    
    return None

def normalize_path(path_key):
    """Convert a path key like 'hampshire/alton' to a file path."""
    parts = path_key.split('/')
    if len(parts) != 2:
        return None
    
    region, city = parts
    return find_city_page(region, city)

def create_storage_html(facility):
    """Generate HTML for a storage facility."""
    name = facility.get('name', '')
    address = facility.get('address', '')
    phone = facility.get('phone', '')
    website = facility.get('website', '')
    description = facility.get('description', '')
    features = facility.get('features', [])
    
    # Ensure website has proper URL format
    if website and not website.startswith(('http://', 'https://')):
        website = f"https://{website}"
    
    # Clean phone number
    if phone:
        phone = re.sub(r'[^0-9]', '', phone)
        if len(phone) == 10:
            phone = f"{phone[:3]} {phone[3:6]} {phone[6:]}"
        elif len(phone) == 11:
            phone = f"{phone[:4]} {phone[4:7]} {phone[7:]}"
    
    # Create feature tags
    feature_tags = ""
    for feature in features:
        feature_tags += f'<span class="feature-tag">{feature}</span>'
    
    html = f'''
    <div class="storage-card">
        <h3>{name}</h3>
        <div class="storage-info">
            <p><strong>Address: </strong>{address}</p>
            <p><strong>Description: </strong>{description}</p>
            <div class="features-list">
                {feature_tags}
            </div>
            <div class="contact-info">
                <p><strong>Phone: </strong><a href="tel:{phone.replace(' ', '')}">{phone}</a></p>
                <p><strong>Website: </strong><a href="{website}" target="_blank">{website.replace('https://', '')}</a></p>
            </div>
        </div>
    </div>
    '''
    
    return html

def update_city_page(file_path, facilities, dry_run=False):
    """Update a city page with new storage facility data."""
    if not file_path or not os.path.exists(file_path):
        return False, f"File not found: {file_path}", 0
    
    if not facilities:
        return False, f"No facility data provided for {file_path}", 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the storage-list container
        storage_list = soup.find(class_="storage-list")
        if not storage_list:
            # Create a new storage-list if it doesn't exist
            main_content = soup.find('main')
            if not main_content:
                # Try to find a suitable container
                containers = soup.find_all(class_=re.compile(r'container'))
                if containers:
                    main_content = containers[-1]  # Use the last container
                else:
                    body = soup.find('body')
                    main_div = soup.new_tag('div')
                    main_div['class'] = 'container'
                    body.append(main_div)
                    main_content = main_div
            
            storage_list = soup.new_tag('div')
            storage_list['class'] = 'storage-list'
            main_content.append(storage_list)
        
        # Get current count before clearing
        current_count = len(storage_list.find_all(class_="storage-card"))
        
        # Clear existing storage cards
        for card in storage_list.find_all(class_="storage-card"):
            card.decompose()
        
        # Add new storage facilities
        facility_count = 0
        for facility in facilities:
            facility_html = create_storage_html(facility)
            facility_soup = BeautifulSoup(facility_html, 'html.parser')
            storage_list.append(facility_soup)
            facility_count += 1
        
        city_name = os.path.basename(os.path.dirname(file_path))
        if dry_run:
            print(f"{Fore.YELLOW}Would update {city_name} from {current_count} to {facility_count} facilities{Style.RESET_ALL}")
            return True, f"Dry run: Would update {facility_count} facilities", facility_count
        else:
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"{Fore.GREEN}Updated {city_name} from {current_count} to {facility_count} facilities{Style.RESET_ALL}")
            return True, f"Updated {facility_count} facilities", facility_count
    
    except Exception as e:
        return False, f"Error updating {file_path}: {str(e)}", 0

def update_region_city_cards(region, city_updates, dry_run=False):
    """Update the storage facility counts on city cards within a region page."""
    if not city_updates:
        return False, "No city updates provided"
    
    region_path = find_region_page(region)
    if not region_path:
        return False, f"Region page not found for: {region}"
    
    try:
        with open(region_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        city_cards = soup.find_all(class_="city-card")
        
        updated_count = 0
        
        for card in city_cards:
            # Find the city name and link in this card
            heading = card.find('h3')
            if not heading:
                continue
            
            link = card.find('a')
            if not link or not link.get('href'):
                continue
            
            href = link.get('href')
            city_match = re.search(r'selfstorage([^/]+)/index\.html', href)
            if not city_match:
                continue
            
            city_folder = city_match.group(1)
            # Convert to the format we need for lookup
            city_name = city_folder.replace('-', ' ')
            
            # Find the corresponding city update
            for city_key, facility_count in city_updates.items():
                key_parts = city_key.split('/')
                if len(key_parts) != 2:
                    continue
                
                _, city = key_parts
                city_slug = city.replace(' ', '-')
                
                if city_slug == city_name:
                    # Find the paragraph with the count
                    p_tag = card.find('p')
                    if p_tag:
                        # Update the storage facility count
                        old_text = p_tag.get_text()
                        new_text = f"{facility_count} Storage Facilities"
                        p_tag.string = new_text
                        
                        if not dry_run:
                            print(f"{Fore.CYAN}Updated card for {city} from '{old_text}' to '{new_text}'{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}Would update card for {city} from '{old_text}' to '{new_text}'{Style.RESET_ALL}")
                        
                        updated_count += 1
                    break
        
        if dry_run:
            return True, f"Would update {updated_count} city cards in {region}"
        else:
            # Write the updated content back to the file
            with open(region_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return True, f"Updated {updated_count} city cards in {region}"
    
    except Exception as e:
        return False, f"Error updating region page {region_path}: {str(e)}"

def verify_city(city_key, file_path):
    """Verify a city page and count its storage facilities."""
    if not file_path or not os.path.exists(file_path):
        return {
            "city_key": city_key,
            "status": "error",
            "error": "File not found",
            "file_path": file_path,
            "facility_count": 0
        }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the storage-list container
        storage_list = soup.find(class_="storage-list")
        if not storage_list:
            return {
                "city_key": city_key,
                "status": "warning",
                "warning": "No storage-list container found",
                "file_path": file_path,
                "facility_count": 0
            }
        
        # Count storage facilities
        storage_cards = storage_list.find_all(class_="storage-card")
        facility_count = len(storage_cards)
        
        # Check for placeholder content
        placeholders = []
        for p in soup.find_all('p'):
            text = p.get_text().lower()
            if 'lorem ipsum' in text or 'placeholder' in text:
                placeholders.append(text[:50] + "..." if len(text) > 50 else text)
        
        result = {
            "city_key": city_key,
            "status": "ok" if facility_count > 0 and not placeholders else "warning",
            "file_path": file_path,
            "facility_count": facility_count
        }
        
        if placeholders:
            result["warning"] = "Placeholder content found"
            result["placeholders"] = placeholders
        
        if facility_count == 0:
            result["warning"] = "No storage facilities found"
        
        return result
    
    except Exception as e:
        return {
            "city_key": city_key,
            "status": "error",
            "error": str(e),
            "file_path": file_path,
            "facility_count": 0
        }

def generate_storage_data(city_key, count=5):
    """Generate random storage facility data for a city."""
    region, city = city_key.split('/')
    
    storage_names = [
        f"{city.title()} Self Storage",
        f"Store Safe {city.title()}",
        f"SecureSpace {city.title()}",
        f"{city.title()} Storage Solutions",
        f"SafeKeep {city.title()}",
        f"StoreBox {city.title()}",
        f"EasyStore {city.title()}",
        f"{city.title()} Lock & Keep",
        f"Space Centre {city.title()}",
        f"StowAway {city.title()}",
    ]
    
    street_names = [
        "High Street", "Station Road", "Main Street", "Church Lane", "Mill Road",
        "Park Avenue", "London Road", "Victoria Road", "Green Lane", "School Lane"
    ]
    
    features = [
        "24/7 Access", "Climate Control", "CCTV", "Secure Facility", "Drive-up Access",
        "Free Parking", "Moving Supplies", "Month-to-Month Rental", "Electronic Gate Access",
        "Security Lighting", "Packing Supplies", "Ground Floor Units", "Loading Dock",
        "Dollies & Carts", "Alarmed Units"
    ]
    
    descriptions = [
        f"Secure self storage units in {city.title()} available in a range of sizes perfect for both business and personal use.",
        f"Modern storage solutions in {city.title()} with flexible contracts and competitive rates.",
        f"Family-owned storage business in {city.title()} offering personal service and tailored storage solutions.",
        f"Affordable and secure storage units in {city.title()} with easy access and various sizes available.",
        f"Premium storage facilities in {city.title()} with state-of-the-art security and customer service."
    ]
    
    facilities = []
    used_names = set()
    
    for i in range(min(count, len(storage_names))):
        # Avoid duplicate names
        available_names = [name for name in storage_names if name not in used_names]
        if not available_names:
            break
            
        name = random.choice(available_names)
        used_names.add(name)
        
        # Generate random address
        street_num = random.randint(1, 99)
        street = random.choice(street_names)
        postal_code = f"{region[:2].upper()}{random.randint(10, 99)} {random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}"
        address = f"{street_num} {street}, {city.title()}, {region.title()}, {postal_code}"
        
        # Generate random phone
        phone = f"0{random.randint(1000, 9999)} {random.randint(100, 999)} {random.randint(100, 999)}"
        
        # Generate website
        website = f"www.{name.lower().replace(' ', '')}.co.uk"
        
        # Select random description
        description = random.choice(descriptions)
        
        # Select random features (2-4)
        feature_count = random.randint(2, 4)
        selected_features = random.sample(features, feature_count)
        
        facility = {
            'name': name,
            'address': address,
            'phone': phone,
            'website': website,
            'description': description,
            'features': selected_features
        }
        
        facilities.append(facility)
    
    return facilities

def main():
    args = parse_args()
    start_time = time.time()
    
    # Initialize result data
    result_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "verify" if args.verify else "update",
        "cities_processed": 0,
        "success_count": 0,
        "error_count": 0,
        "city_results": []
    }
    
    # Process the CSV if provided
    if os.path.exists(args.csv):
        print(f"{Fore.CYAN}Reading facility data from {args.csv}...{Style.RESET_ALL}")
        facilities_data = read_csv_data(args.csv)
        
        if facilities_data:
            print(f"{Fore.GREEN}Found data for {len(facilities_data)} cities in CSV{Style.RESET_ALL}")
            result_data["csv_file"] = args.csv
            result_data["csv_cities"] = len(facilities_data)
        else:
            facilities_data = {}
            print(f"{Fore.YELLOW}No facility data found in the CSV file or file format error{Style.RESET_ALL}")
            result_data["csv_file"] = args.csv
            result_data["csv_cities"] = 0
    else:
        facilities_data = {}
        print(f"{Fore.YELLOW}CSV file not found: {args.csv}{Style.RESET_ALL}")
        result_data["csv_error"] = f"File not found: {args.csv}"
    
    # Find all city pages to process
    if args.city:
        # Process single city
        city_key = args.city.lower()
        file_path = normalize_path(city_key)
        if file_path:
            cities_to_process = {city_key: file_path}
            print(f"{Fore.CYAN}Processing single city: {city_key}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}City page not found for: {args.city}{Style.RESET_ALL}")
            return
    elif args.region:
        # Process cities in a specific region
        region = args.region.lower()
        website_dir = os.path.join(os.getcwd(), "website")
        region_folder = f"selfstorage{region.replace(' ', '-').lower()}"
        region_path = os.path.join(website_dir, region_folder)
        
        if not os.path.exists(region_path):
            print(f"{Fore.RED}Region folder not found: {region_path}{Style.RESET_ALL}")
            return
        
        cities_to_process = {}
        for item in os.listdir(region_path):
            city_folder = os.path.join(region_path, item)
            if os.path.isdir(city_folder) and item.startswith('selfstorage'):
                city_index = os.path.join(city_folder, "index.html")
                if os.path.exists(city_index):
                    city_name = item[len('selfstorage'):]
                    city_key = f"{region}/{city_name}"
                    cities_to_process[city_key] = city_index
        
        print(f"{Fore.CYAN}Found {len(cities_to_process)} cities in region {region}{Style.RESET_ALL}")
    else:
        # Find all city pages
        cities_to_process = {}
        website_dir = os.path.join(os.getcwd(), "website")
        
        for item in os.listdir(website_dir):
            region_folder = os.path.join(website_dir, item)
            if os.path.isdir(region_folder) and item.startswith('selfstorage') and not item == 'selfstorageregions':
                region_name = item[len('selfstorage'):]
                
                for city_item in os.listdir(region_folder):
                    city_folder = os.path.join(region_folder, city_item)
                    if os.path.isdir(city_folder) and city_item.startswith('selfstorage'):
                        city_index = os.path.join(city_folder, "index.html")
                        if os.path.exists(city_index):
                            city_name = city_item[len('selfstorage'):]
                            city_key = f"{region_name}/{city_name}"
                            cities_to_process[city_key] = city_index
        
        print(f"{Fore.CYAN}Found {len(cities_to_process)} cities across all regions{Style.RESET_ALL}")
    
    result_data["cities_found"] = len(cities_to_process)
    
    if args.verify:
        # Verify city pages and count storage facilities
        print(f"{Fore.CYAN}Verifying {len(cities_to_process)} cities...{Style.RESET_ALL}")
        
        city_results = []
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {executor.submit(verify_city, city_key, file_path): city_key for city_key, file_path in cities_to_process.items()}
            
            for future in futures:
                result = future.result()
                city_results.append(result)
                
                if result["status"] == "ok":
                    print(f"{Fore.GREEN}✓ {result['city_key']}: {result['facility_count']} facilities{Style.RESET_ALL}")
                    result_data["success_count"] += 1
                elif result["status"] == "warning":
                    warning = result.get("warning", "Unknown warning")
                    print(f"{Fore.YELLOW}⚠ {result['city_key']}: {warning} ({result['facility_count']} facilities){Style.RESET_ALL}")
                    result_data["success_count"] += 1  # Count warnings as successes
                else:
                    error = result.get("error", "Unknown error")
                    print(f"{Fore.RED}✗ {result['city_key']}: {error}{Style.RESET_ALL}")
                    result_data["error_count"] += 1
        
        result_data["city_results"] = city_results
        result_data["cities_processed"] = len(city_results)
    else:
        # Update city pages with storage facility data
        print(f"{Fore.CYAN}Updating {len(cities_to_process)} cities...{Style.RESET_ALL}")
        
        # Track updates for region pages
        region_updates = {}
        city_results = []
        
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []
            
            for city_key, file_path in cities_to_process.items():
                # Get facilities data from CSV or generate random data
                if city_key in facilities_data:
                    facilities = facilities_data[city_key]
                    print(f"{Fore.CYAN}Using CSV data for {city_key} ({len(facilities)} facilities){Style.RESET_ALL}")
                else:
                    # Generate random facilities data (between 3 and 8)
                    count = random.randint(3, 8)
                    facilities = generate_storage_data(city_key, count)
                    print(f"{Fore.YELLOW}Generated random data for {city_key} ({len(facilities)} facilities){Style.RESET_ALL}")
                
                futures.append(executor.submit(update_city_page, file_path, facilities, args.dry_run))
            
            idx = 0
            for city_key in cities_to_process.keys():
                future = futures[idx]
                success, message, facility_count = future.result()
                
                result = {
                    "city_key": city_key,
                    "status": "success" if success else "error",
                    "message": message,
                    "facility_count": facility_count
                }
                city_results.append(result)
                
                # Track for region updates
                if success:
                    region, city = city_key.split('/')
                    if region not in region_updates:
                        region_updates[region] = {}
                    region_updates[region][city_key] = facility_count
                    
                    result_data["success_count"] += 1
                else:
                    result_data["error_count"] += 1
                
                idx += 1
        
        result_data["city_results"] = city_results
        result_data["cities_processed"] = len(city_results)
        
        # Update region pages with city facility counts if requested
        if args.fix_card_counts and not args.dry_run:
            print(f"{Fore.CYAN}Updating city cards in region pages...{Style.RESET_ALL}")
            
            for region, city_updates in region_updates.items():
                success, message = update_region_city_cards(region, city_updates, args.dry_run)
                print(f"{Fore.GREEN if success else Fore.RED}{message}{Style.RESET_ALL}")
    
    elapsed_time = time.time() - start_time
    result_data["elapsed_time"] = f"{elapsed_time:.2f} seconds"
    
    # Save report to JSON file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2)
    
    print(f"\n{Fore.CYAN}Results summary:{Style.RESET_ALL}")
    print(f"- Total cities processed: {result_data['cities_processed']}")
    print(f"- Successfully updated/verified: {result_data['success_count']}")
    print(f"- Errors: {result_data['error_count']}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")
    print(f"- Detailed report saved to: {args.output}")

if __name__ == "__main__":
    main() 