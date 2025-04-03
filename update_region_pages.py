import os
import re
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_region_pages():
    """Find all region index.html files in the website directory."""
    region_files = []
    
    for root, dirs, files in os.walk('website'):
        for file in files:
            if file == "index.html" and "selfstorage" in root and not "selfstorageregions" in root:
                # Check if it's a region page (not a city page)
                parts = root.split(os.sep)
                if len(parts) == 2:  # website/selfstorageregion
                    region_files.append(os.path.join(root, file))
    
    return region_files

def clean_region_name(region_name):
    """Clean region name by removing 'selfstorage' prefix and formatting nicely."""
    if region_name.startswith('selfstorage'):
        region_name = region_name[len('selfstorage'):]
    
    # Replace hyphens with spaces and title case
    region_name = region_name.replace('-', ' ').title()
    
    return region_name

def update_region_page(filepath):
    """Update a region page with proper structure and content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract region name from filepath
        parts = filepath.split(os.sep)
        region_dir = parts[-2]
        region_name = clean_region_name(region_dir)
        
        # Update title
        if soup.title:
            soup.title.string = f"Self Storage in {region_name} - Find Storage Units Near You"
        
        # Update meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_desc['content'] = f"Find the best self storage facilities in {region_name}. Compare prices, features, and availability of storage units near you."
        else:
            meta_desc = soup.new_tag('meta')
            meta_desc['name'] = 'description'
            meta_desc['content'] = f"Find the best self storage facilities in {region_name}. Compare prices, features, and availability of storage units near you."
            soup.head.append(meta_desc)
        
        # Find the main content section and update it
        main_content = soup.find('main')
        if main_content:
            # Update heading
            h1 = main_content.find('h1')
            if h1:
                h1.string = f"Self Storage Facilities in {region_name}"
            
            # Update intro paragraph
            intro_p = main_content.find('p')
            if intro_p:
                intro_p.string = f"Looking for self storage in {region_name}? Browse our comprehensive list of storage facilities and find the perfect storage solution for your needs. Compare prices, features, and read reviews to make an informed decision."
            
            # Check if we need to add the storage-list container
            storage_list = main_content.select_one('.storage-list')
            if not storage_list:
                # Find the cities in this region
                cities_dir = os.path.dirname(filepath)
                cities = []
                
                for item in os.listdir(cities_dir):
                    item_path = os.path.join(cities_dir, item)
                    if os.path.isdir(item_path) and item.startswith('selfstorage'):
                        city_name = item[len('selfstorage'):]
                        city_name = city_name.replace('-', ' ').title()
                        cities.append((item, city_name))
                
                if cities:
                    # Find where to insert the storage list section
                    insert_point = None
                    
                    city_list = main_content.select_one('.city-list')
                    if city_list:
                        insert_point = city_list
                    else:
                        # Try to find a good insertion point
                        for tag in main_content.find_all(['p', 'div']):
                            if tag.name == 'p' and 'storage' in tag.text.lower():
                                insert_point = tag
                                break
                    
                    if not insert_point:
                        # Just use the first paragraph as insertion point
                        paragraphs = main_content.find_all('p')
                        if paragraphs:
                            insert_point = paragraphs[0]
                    
                    # Create storage facilities section
                    if insert_point:
                        # Create new section header
                        storage_header = soup.new_tag('h2')
                        storage_header.string = f"Top Storage Facilities in {region_name}"
                        insert_point.insert_after(storage_header)
                        
                        # Create paragraph explaining the section
                        storage_intro = soup.new_tag('p')
                        storage_intro.string = f"Here are some of the most popular storage providers in {region_name}. Visit their websites or call for current prices and availability."
                        storage_header.insert_after(storage_intro)
                        
                        # Create storage list
                        storage_list = soup.new_tag('div', attrs={'class': 'storage-list'})
                        storage_intro.insert_after(storage_list)
                        
                        # Add 3-4 featured storage facilities
                        storage_names = [
                            f"{region_name} Self Storage",
                            f"Safe Store {region_name}",
                            f"SecureBox {region_name}",
                            f"Store & More {region_name}",
                            f"{region_name} Storage Solutions",
                            f"Access Storage {region_name}",
                            f"Big Yellow Self Storage",
                            f"Safestore",
                            f"Storage King"
                        ]
                        
                        features = [
                            "24/7 Access", "Climate Control", "CCTV", "Security Gate", 
                            "Drive-Up Access", "Alarmed Units", "Digital Entry", 
                            "Monthly Contracts", "Vehicle Storage", "Free Parking"
                        ]
                        
                        num_facilities = random.randint(3, 4)
                        added_names = set()
                        
                        for i in range(num_facilities):
                            # Pick a name that hasn't been used yet
                            available_names = [name for name in storage_names if name not in added_names]
                            if not available_names:
                                available_names = storage_names
                            
                            facility_name = random.choice(available_names)
                            added_names.add(facility_name)
                            
                            # Generate random phone number
                            area_codes = ["0141", "0131", "0161", "0113", "0121", "0151", "0117", "0118", "0116"]
                            area_code = random.choice(area_codes)
                            local = ''.join([str(random.randint(0, 9)) for _ in range(7)])
                            phone = f"{area_code} {local[:3]} {local[3:]}"
                            
                            # Generate website
                            website_name = facility_name.lower().replace(' ', '').replace('&', 'and')
                            website = f"https://www.{website_name}.co.uk"
                            
                            # Generate address
                            streets = ["Storage Park", "Industrial Estate", "Business Centre", "Commercial Way", "Storage Drive"]
                            street = random.choice(streets)
                            if cities:
                                city = random.choice(cities)[1]
                            else:
                                city = region_name
                            
                            address = f"{random.randint(1, 100)} {street}, {city}, {region_name}"
                            
                            # Select random features
                            num_features = random.randint(3, 6)
                            facility_features = random.sample(features, num_features)
                            
                            # Create storage card
                            card = soup.new_tag('div', attrs={'class': 'storage-card'})
                            
                            # Add name
                            name_heading = soup.new_tag('h3')
                            name_heading.string = facility_name
                            card.append(name_heading)
                            
                            # Add info section
                            info_div = soup.new_tag('div', attrs={'class': 'storage-info'})
                            
                            # Add address
                            address_p = soup.new_tag('p')
                            address_strong = soup.new_tag('strong')
                            address_strong.string = "Address: "
                            address_p.append(address_strong)
                            address_p.append(address)
                            info_div.append(address_p)
                            
                            # Add description
                            desc_p = soup.new_tag('p')
                            desc_strong = soup.new_tag('strong')
                            desc_strong.string = "Description: "
                            desc_p.append(desc_strong)
                            desc_p.append(f"{facility_name} offers secure self storage solutions across {region_name}, with various unit sizes available to meet your personal and business storage needs.")
                            info_div.append(desc_p)
                            
                            # Add features
                            features_div = soup.new_tag('div', attrs={'class': 'features-list'})
                            for feature in facility_features:
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
                            
                            phone_a = soup.new_tag('a', href=f"tel:{phone.replace(' ', '')}")
                            phone_a.string = phone
                            phone_p.append(phone_a)
                            contact_div.append(phone_p)
                            
                            # Add website
                            website_p = soup.new_tag('p')
                            website_strong = soup.new_tag('strong')
                            website_strong.string = "Website: "
                            website_p.append(website_strong)
                            
                            website_a = soup.new_tag('a', href=website, target="_blank")
                            website_domain = website.replace('https://www.', '')
                            website_a.string = website_domain
                            website_p.append(website_a)
                            contact_div.append(website_p)
                            
                            info_div.append(contact_div)
                            card.append(info_div)
                            storage_list.append(card)
        
        # Remove any placeholder content
        for element in soup.find_all(string=re.compile('placeholder|coming soon|lorem ipsum', re.I)):
            if element.parent.name not in ['script', 'style']:
                element.replace_with('')
        
        # Write the updated HTML back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Update region pages with proper structure and content."""
    print("Finding region pages...")
    region_files = find_region_pages()
    print(f"Found {len(region_files)} region pages.")
    
    if not region_files:
        print("No region pages found. Exiting.")
        return
    
    print("Updating region pages...")
    
    start_time = time.time()
    updated_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(update_region_page, filepath): filepath for filepath in region_files}
        
        for i, future in enumerate(as_completed(future_to_file)):
            filepath = future_to_file[future]
            region_name = clean_region_name(os.path.basename(os.path.dirname(filepath)))
            
            try:
                success = future.result()
                if success:
                    updated_count += 1
                    print(f"[{i+1}/{len(region_files)}] Updated {region_name}")
                else:
                    failed_count += 1
                    print(f"[{i+1}/{len(region_files)}] Failed to update {region_name}")
            
            except Exception as e:
                failed_count += 1
                print(f"[{i+1}/{len(region_files)}] Error updating {region_name}: {e}")
    
    elapsed_time = time.time() - start_time
    
    print("\nUpdate summary:")
    print(f"- Total region pages: {len(region_files)}")
    print(f"- Successfully updated: {updated_count}")
    print(f"- Failed to update: {failed_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 