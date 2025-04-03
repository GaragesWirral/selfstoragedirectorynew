import pandas as pd
import os
import re
from bs4 import BeautifulSoup
import random
import sys

# Set to process specific regions by default
TARGET_REGIONS = ["Hampshire", "Wiltshire"]
PROCESS_ALL_REGIONS = False

# If command line argument is provided, check if it's "all"
if len(sys.argv) > 1:
    if sys.argv[1].lower() == "all":
        PROCESS_ALL_REGIONS = True
        TARGET_REGIONS = []
    else:
        # Accept region names as command-line arguments
        TARGET_REGIONS = [arg for arg in sys.argv[1:]]

def clean_city_name(city):
    """Clean city name by removing trailing characters and 'Bedfordshire' suffix."""
    city = str(city).strip()
    # Remove non-alphanumeric characters at the end (like ‎)
    city = re.sub(r'[^\w\s]+$', '', city)
    # Remove ", Bedfordshire" or similar suffixes
    city = re.sub(r',\s*[A-Za-z]+$', '', city)
    return city.strip()

def get_features():
    """Generate random features for a storage facility."""
    all_features = [
        "24/7 Access", "Climate Control", "CCTV", "Vehicle Storage",
        "Drive-up Access", "Business Storage", "Alarmed Units", 
        "Moving Supplies", "Packing Materials", "Student Storage",
        "Free Collection", "Indoor Units", "Outdoor Units", "Container Storage",
        "Secure Facility", "Insurance Available", "Long-term Discounts",
        "Short-term Storage", "Document Storage", "Furniture Storage"
    ]
    
    # Select 3-5 random features
    num_features = random.randint(3, 5)
    return random.sample(all_features, num_features)

def get_website_link(website_url):
    """Format website URL into a proper link."""
    if pd.isna(website_url) or not website_url:
        return "#", "Contact for website"
    
    # Cleanup URL
    website_url = str(website_url).strip()
    
    # Extract domain name for display
    domain = website_url
    if "//" in domain:
        domain = domain.split("//")[1]
    if "/" in domain:
        domain = domain.split("/")[0]
    
    return website_url, domain

def get_phone_link(phone_number):
    """Format phone number into a proper link."""
    if pd.isna(phone_number) or not phone_number:
        return "#", "Contact for phone"
    
    # Clean up phone number - just take the first one if multiple
    phone_number = str(phone_number)
    if "\n" in phone_number:
        phone_number = phone_number.split("\n")[0]
    
    # Remove non-numeric characters for href but keep original for display
    clean_number = re.sub(r'\D', '', phone_number)
    if clean_number.startswith("44"):
        clean_number = "0" + clean_number[2:]  # Convert +44 to 0
    
    return f"tel:{clean_number}", phone_number

def format_location(location):
    """Format the location string to be more readable."""
    if pd.isna(location) or not location:
        return "Contact for address"
    
    location = str(location)
    # Replace newlines with commas
    location = location.replace("\n", ", ")
    
    # Clean up multiple commas/spaces
    location = re.sub(r',\s*,', ',', location)
    location = re.sub(r'\s+', ' ', location)
    
    return location

def update_city_page(region, city, facilities_data):
    """Update a city page with real storage facility data."""
    try:
        # Normalize inputs
        region = region.lower().replace(' ', '')
        clean_city = clean_city_name(city).lower().replace(' ', '')
        clean_city = re.sub(r'[^\w]', '', clean_city)  # Remove any non-alphanumeric chars
        
        # Define the path to the HTML file
        file_path = f"website/selfstorage{region}/selfstorage{clean_city}/index.html"
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Find the storage-list div
        storage_list = soup.select_one('.storage-list')
        if not storage_list:
            print(f"Storage list not found in {file_path}")
            return False
        
        # Clear existing storage cards
        storage_list.clear()
        
        # Add real storage facilities
        facility_count = 0
        for _, facility in facilities_data.iterrows():
            try:
                # Create a new storage card
                storage_card = soup.new_tag('div', attrs={'class': 'storage-card'})
                
                # Add facility name
                name = facility['Name of Self Storage']
                if pd.isna(name) or not name:
                    name = "Storage Facility"
                h3 = soup.new_tag('h3')
                h3.string = str(name)
                storage_card.append(h3)
                
                # Add facility info container
                info_div = soup.new_tag('div', attrs={'class': 'storage-info'})
                
                # Add address
                address_p = soup.new_tag('p')
                address_strong = soup.new_tag('strong')
                address_strong.string = "Address: "
                address_p.append(address_strong)
                address_p.append(format_location(facility['Location']))
                info_div.append(address_p)
                
                # Add description
                desc_p = soup.new_tag('p')
                desc_strong = soup.new_tag('strong')
                desc_strong.string = "Description: "
                desc_p.append(desc_strong)
                
                # Generate a description if none is provided
                description = f"{name} offers self storage solutions in {city}, with various unit sizes available to meet your personal and business storage needs."
                desc_p.append(description)
                info_div.append(desc_p)
                
                # Add features
                features_div = soup.new_tag('div', attrs={'class': 'features-list'})
                for feature in get_features():
                    feature_span = soup.new_tag('span', attrs={'class': 'feature-tag'})
                    feature_span.string = feature
                    features_div.append(feature_span)
                info_div.append(features_div)
                
                # Add contact info
                contact_div = soup.new_tag('div', attrs={'class': 'contact-info'})
                
                # Add phone
                phone_p = soup.new_tag('p')
                phone_strong = soup.new_tag('strong')
                phone_strong.string = "Phone: "
                phone_p.append(phone_strong)
                
                phone_href, phone_display = get_phone_link(facility['Telephone Number'])
                phone_a = soup.new_tag('a', href=phone_href)
                phone_a.string = phone_display
                phone_p.append(phone_a)
                contact_div.append(phone_p)
                
                # Add website
                website_p = soup.new_tag('p')
                website_strong = soup.new_tag('strong')
                website_strong.string = "Website: "
                website_p.append(website_strong)
                
                website_href, website_display = get_website_link(facility['Website'])
                website_a = soup.new_tag('a', href=website_href, target="_blank")
                website_a.string = website_display
                website_p.append(website_a)
                contact_div.append(website_p)
                
                info_div.append(contact_div)
                storage_card.append(info_div)
                storage_list.append(storage_card)
                facility_count += 1
            except Exception as e:
                print(f"Error processing facility {_}: {e}")
                continue
        
        # Write the updated HTML back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Updated {file_path} with {facility_count} facilities")
        return True
    
    except Exception as e:
        print(f"Error updating {region}/{city}: {e}")
        return False

def main():
    # Read the Excel file
    try:
        excel_data = pd.read_excel("self storage facilities uk.xlsx")
        print(f"Read {len(excel_data)} facilities from Excel file")
        
        # Process target regions
        for region in TARGET_REGIONS:
            region_data = excel_data[excel_data['Region'] == region]
            
            # Group by city
            cities = region_data.groupby('CITY')
            
            print(f"Found {len(cities)} cities in {region}")
            
            # Process each city
            for city, facilities in cities:
                clean_city = clean_city_name(city)
                print(f"Processing {clean_city} with {len(facilities)} facilities")
                update_city_page(region, clean_city, facilities)
            
            print(f"Finished updating {region} cities")
        
        # Process all regions if requested
        if PROCESS_ALL_REGIONS:
            print("\nProcessing all regions...")
            regions = excel_data['Region'].unique()
            for region in regions:
                if pd.isna(region) or region in TARGET_REGIONS:  # Skip regions we already did
                    continue
                    
                print(f"\nProcessing region: {region}")
                region_data = excel_data[excel_data['Region'] == region]
                
                # Group by city
                cities = region_data.groupby('CITY')
                
                print(f"Found {len(cities)} cities in {region}")
                
                # Process each city
                for city, facilities in cities:
                    if pd.isna(city):
                        continue
                    clean_city = clean_city_name(city)
                    print(f"Processing {clean_city} with {len(facilities)} facilities")
                    update_city_page(region, clean_city, facilities)
            
            print("Finished updating all regions")
    
    except Exception as e:
        print(f"Error processing Excel file: {e}")

if __name__ == "__main__":
    main() 