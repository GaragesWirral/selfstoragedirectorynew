import os
import csv
import re
from bs4 import BeautifulSoup
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update storage facilities based on data from a CSV file")
    parser.add_argument("--csv", default="storage_facilities.csv", help="Path to the CSV file containing storage facility data")
    parser.add_argument("--city", help="Specific city to update (format: 'region/city', e.g. 'hampshire/alton')")
    parser.add_argument("--all", action="store_true", help="Update all cities found in the CSV")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--threads", type=int, default=8, help="Number of threads to use for parallel processing")
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
        print(f"Error reading CSV file: {str(e)}")
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
    
    if not website.startswith(('http://', 'https://')):
        website = f"https://{website}"
    
    # Clean phone number
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
        return False, f"File not found: {file_path}"
    
    if not facilities:
        return False, f"No facility data provided for {file_path}"
    
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
        
        if dry_run:
            city_name = os.path.basename(os.path.dirname(file_path))
            print(f"Would update {city_name} with {facility_count} facilities")
            return True, f"Dry run: Would update {facility_count} facilities"
        else:
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            city_name = os.path.basename(os.path.dirname(file_path))
            print(f"Updated {city_name} with {facility_count} facilities")
            return True, f"Updated {facility_count} facilities"
    
    except Exception as e:
        return False, f"Error updating {file_path}: {str(e)}"

def main():
    args = parse_args()
    start_time = time.time()
    
    if not os.path.exists(args.csv):
        print(f"CSV file not found: {args.csv}")
        return
    
    print(f"Reading facility data from {args.csv}...")
    facilities_data = read_csv_data(args.csv)
    
    if not facilities_data:
        print("No facility data found in the CSV file")
        return
    
    print(f"Found data for {len(facilities_data)} cities")
    
    # Filter to specific city if requested
    if args.city:
        city_key = args.city.lower()
        if city_key in facilities_data:
            facilities_data = {city_key: facilities_data[city_key]}
        else:
            print(f"No data found for city: {args.city}")
            return
    
    # Process all cities
    success_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        
        for city_key, facilities in facilities_data.items():
            file_path = normalize_path(city_key)
            if file_path:
                futures.append(executor.submit(update_city_page, file_path, facilities, args.dry_run))
            else:
                print(f"City page not found for: {city_key}")
                error_count += 1
        
        for future in futures:
            success, message = future.result()
            if success:
                success_count += 1
            else:
                error_count += 1
                print(f"Error: {message}")
    
    elapsed_time = time.time() - start_time
    
    print("\nUpdate summary:")
    print(f"- Total cities processed: {len(facilities_data)}")
    print(f"- Successfully updated: {success_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 