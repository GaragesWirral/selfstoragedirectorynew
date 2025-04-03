import os
import csv
import re
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

def load_csv_data(csv_file='correct_storage_facilities.csv'):
    """Load storage facility data from CSV file."""
    facilities_by_city = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            region = row['Region'].lower().replace(' ', '')
            city = row['City'].lower().replace(' ', '')
            
            if region not in facilities_by_city:
                facilities_by_city[region] = {}
            
            if city not in facilities_by_city[region]:
                facilities_by_city[region][city] = []
            
            # Parse features into a list
            features = []
            if row['Features']:
                features = [feat.strip() for feat in row['Features'].split(',')]
            
            facility = {
                'name': row['Name'],
                'address': row['Address'],
                'phone': row['Phone'],
                'website': row['Website'],
                'description': row['Description'],
                'features': features
            }
            
            facilities_by_city[region][city].append(facility)
    
    return facilities_by_city

def get_region_directory(region):
    """Get the correct directory name for a region, handling hyphens."""
    # Handle special cases with hyphens
    if region == 'greaterlondon':
        return 'greater-london'
    
    # Try with different formats
    formats = [
        f"selfstorage{region}",
        f"selfstorage{region.replace('shire', '')}",
        f"selfstorage{region.replace('shire', '-shire')}",
        f"selfstorage{'-'.join(re.findall(r'[a-z]+', region))}"  # Add hyphens between words
    ]
    
    for dir_format in formats:
        if os.path.exists(f"website/{dir_format}"):
            return dir_format.replace('selfstorage', '')
    
    # For debugging
    print(f"Could not find directory for region: {region}")
    return region

def update_city_page(region, city, facilities_data):
    """Update a city page with the correct storage facilities."""
    region_dir_name = get_region_directory(region)
    region_dir = f"website/selfstorage{region_dir_name}"
    city_dir = f"{region_dir}/selfstorage{city}"
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
        
        # Add new storage cards based on CSV data
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
            phone = soup.new_tag('p')
            phone_strong = soup.new_tag('strong')
            phone_strong.string = 'Phone: '
            phone.append(phone_strong)
            
            phone_link = soup.new_tag('a', href=f"tel:{facility['phone'].replace(' ', '')}")
            phone_link.string = facility['phone']
            phone.append(phone_link)
            contact.append(phone)
            
            # Add website
            website = soup.new_tag('p')
            website_strong = soup.new_tag('strong')
            website_strong.string = 'Website: '
            website.append(website_strong)
            
            website_link = soup.new_tag('a', href=f"https://{facility['website']}", target="_blank")
            website_link.string = facility['website']
            website.append(website_link)
            contact.append(website)
            
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

def update_region_page(region, cities_data):
    """Update the region page with the correct count of storage facilities per city."""
    region_dir_name = get_region_directory(region)
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
            city_name = card.find('h3').text.lower().replace(' ', '')
            normalized_names = {k.lower().replace(' ', ''): k for k in cities_data.keys()}
            
            # Try to match city name (handle variations like "city-and-surroundings")
            matched_city = None
            for norm_name, orig_name in normalized_names.items():
                if city_name == norm_name or city_name.startswith(norm_name) or norm_name.startswith(city_name):
                    matched_city = orig_name
                    break
            
            if matched_city:
                facilities_count = len(cities_data[matched_city])
                facility_text = f"{facilities_count} Storage {'Facilities' if facilities_count != 1 else 'Facility'}"
                
                # Update the count text
                p_tag = card.find('p')
                if p_tag:
                    if p_tag.text != facility_text:
                        p_tag.string = facility_text
                        print(f"Updated card for {matched_city} from '{p_tag.text}' to '{facility_text}'")
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
    
    # Load data from CSV
    facilities_data = load_csv_data()
    
    total_updated = 0
    errors = 0
    
    # Process one region at a time to handle errors better
    for region, cities in facilities_data.items():
        print(f"\nProcessing region: {region}")
        
        # Update the region page
        update_region_page(region, cities)
        
        # Update each city page
        for city, facilities in cities.items():
            print(f"  Processing city: {city}")
            if update_city_page(region, city, facilities):
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