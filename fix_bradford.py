import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import shutil

def normalize_name(name):
    """Normalize a name by converting to lowercase, removing special characters, and replacing spaces with hyphens."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    return name

def update_bradford():
    """Update the Bradford city page and rename directories."""
    # Define paths
    west_yorkshire_dir = 'website/selfstoragewest-yorkshire'
    old_city_name = 'Bradford (interesting below near low moor)'
    new_city_name = 'Bradford'
    
    # Normalize for directory names
    old_normalized = normalize_name(old_city_name)
    new_normalized = normalize_name(new_city_name)
    
    old_dir = f'{west_yorkshire_dir}/selfstorage{old_normalized}'
    new_dir = f'{west_yorkshire_dir}/selfstorage{new_normalized}'
    
    # Check if the old directory exists
    if os.path.exists(old_dir):
        print(f"Found old directory: {old_dir}")
        # Check if the new directory already exists
        if os.path.exists(new_dir):
            print(f"Warning: New directory already exists: {new_dir}")
            print("Will update existing Bradford page instead of renaming")
        else:
            # Rename the directory
            os.rename(old_dir, new_dir)
            print(f"Renamed directory: {old_dir} -> {new_dir}")
    else:
        print(f"Old directory not found: {old_dir}")
        # Create new directory if it doesn't exist
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            print(f"Created new directory: {new_dir}")
    
    # Update the HTML file for Bradford
    bradford_html_path = f'{new_dir}/index.html'
    
    # Check if the HTML file exists
    if not os.path.exists(bradford_html_path):
        print(f"Bradford HTML file not found: {bradford_html_path}")
        # Copy a template from another city if needed
        template_city_path = f'{west_yorkshire_dir}/selfstorageleeds/index.html'
        if os.path.exists(template_city_path):
            shutil.copy(template_city_path, bradford_html_path)
            print(f"Created Bradford HTML file from template: {bradford_html_path}")
        else:
            print("Error: Could not find a template to create Bradford HTML file")
            return
    
    # Read the Bradford HTML file
    with open(bradford_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Update the title and heading
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = 'Self Storage in Bradford, West Yorkshire - Find Storage Units Near You'
    
    h1_tag = soup.find('h1')
    if h1_tag:
        h1_tag.string = 'Self Storage in Bradford, West Yorkshire'
    
    # Update breadcrumbs
    span_tags = soup.find_all('span')
    for span in span_tags:
        if 'Bradford' in span.text or 'bradford' in span.text.lower():
            span.string = 'Bradford'
    
    # Update H2 heading
    h2_tags = soup.find_all('h2')
    for h2 in h2_tags:
        if 'Storage Providers' in h2.text:
            h2.string = 'Storage Providers in Bradford'
    
    # Find the storage-list div
    storage_list = soup.find('div', class_='storage-list')
    if not storage_list:
        print("Storage list not found in Bradford HTML file")
        storage_list = soup.new_tag('div', attrs={'class': 'storage-list'})
        
        # Find container div to add the storage list
        container = soup.find('div', class_='container')
        if container:
            container.append(storage_list)
    else:
        # Clear existing storage cards
        storage_list.clear()
    
    # Define the Bradford storage facilities
    bradford_facilities = [
        {
            'name': 'The Store Room',
            'website': 'www.thestoreroom.co.uk/storage-bradford/',
            'email': 'bradford@thestoreroom.co.uk',
            'phone': '01274 575 369',
            'address': 'Beckside Road, Bradford, BD7 2JS'
        },
        {
            'name': 'Stadium Storage',
            'website': 'stadiumstorage.co.uk/',
            'email': 'bradford@stadiumstorage.co.uk',
            'phone': '01274 667 765',
            'address': 'Sticker Lane Trade Park\nSticker Lane\nBradford\nBD4 8QD'
        },
        {
            'name': 'Incredible Bulk Self Storage',
            'website': 'incrediblebulkstorage.co.uk/',
            'email': 'info@incrediblebulkstorage.co.uk',
            'phone': '01274 975678',
            'address': 'Unit 9A, Whetley Mills,\nThornton Road,\nBradford,\nBD8 8LQ'
        },
        {
            'name': "BOYLIN'S SELF STORE BRADFORD",
            'website': 'www.boylinsselfstore.co.uk/locations/bradford.htm',
            'email': 'info@boylinsselfstore.co.uk',
            'phone': '01274 737597',
            'address': 'Teasdale Street, Off Wakefield Road,\nBradford BD4 7QJ'
        },
        {
            'name': 'Bradford Ring Road Self Storage',
            'website': '',
            'email': '',
            'phone': '',
            'address': 'Bradford, West Yorkshire'
        },
        {
            'name': 'Titan Self Storage',
            'website': 'titancontainers.co.uk/self-storage/north-east/bradford/',
            'email': '',
            'phone': '',
            'address': 'Former BOC site, Duncombe Rd, Bradford BD8 9TB'
        },
        {
            'name': '1st Class Storage',
            'website': '1stclass-storage.co.uk/',
            'email': '',
            'phone': '',
            'address': 'Unit 11, Park, The Iron Works, Bowling Back Ln, Bradford BD4 8SX'
        },
        {
            'name': 'Wilsden Self Storage',
            'website': 'www.wilsdenselfstorage.co.uk/',
            'email': 'info@wilsdenselfstorage.co.uk',
            'phone': '01535 275594',
            'address': 'Well House Mill,\nMain Street,\nWilsden,\nBradford\nBD15 0JW'
        },
        {
            'name': 'Selfie Storage',
            'website': 'selfiestorage.co.uk/',
            'email': 'info@selfiestorage.co.uk',
            'phone': '01274 411089',
            'address': 'Central Place, Clayton, Bradford, BD14 6A'
        }
    ]
    
    # Add the storage facilities to the page
    for facility in bradford_facilities:
        # Create description
        description = f"{facility['name']} provides self storage solutions in Bradford, West Yorkshire. Located at {facility['address']} with easy access and secure storage options."
        
        # Create a new storage card
        card = soup.new_tag('div', attrs={'class': 'storage-card'})
        
        # Add facility name
        name_tag = soup.new_tag('h3')
        name_tag.string = facility['name']
        card.append(name_tag)
        
        # Create storage info container
        info = soup.new_tag('div', attrs={'class': 'storage-info'})
        
        # Add address
        address_p = soup.new_tag('p')
        address_strong = soup.new_tag('strong')
        address_strong.string = 'Address: '
        address_p.append(address_strong)
        address_p.append(facility['address'])
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
        if facility['phone']:
            phone_p = soup.new_tag('p')
            phone_strong = soup.new_tag('strong')
            phone_strong.string = 'Phone: '
            phone_p.append(phone_strong)
            
            phone_link = soup.new_tag('a', href=f"tel:{facility['phone'].replace(' ', '')}")
            phone_link.string = facility['phone']
            phone_p.append(phone_link)
            contact.append(phone_p)
        
        # Add website
        if facility['website']:
            website_p = soup.new_tag('p')
            website_strong = soup.new_tag('strong')
            website_strong.string = 'Website: '
            website_p.append(website_strong)
            
            website_link = soup.new_tag('a', href=f"https://{facility['website']}", target="_blank")
            website_link.string = facility['website']
            website_p.append(website_link)
            contact.append(website_p)
        
        # Add email
        if facility['email']:
            email_p = soup.new_tag('p')
            email_strong = soup.new_tag('strong')
            email_strong.string = 'Email: '
            email_p.append(email_strong)
            
            email_link = soup.new_tag('a', href=f"mailto:{facility['email']}")
            email_link.string = facility['email']
            email_p.append(email_link)
            contact.append(email_p)
        
        info.append(contact)
        card.append(info)
        storage_list.append(card)
    
    # Update the Bradford HTML file
    with open(bradford_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Successfully updated Bradford page with {len(bradford_facilities)} facilities")
    
    # Now update the West Yorkshire region page
    region_html = f'{west_yorkshire_dir}/index.html'
    
    with open(region_html, 'r', encoding='utf-8') as f:
        region_content = f.read()
    
    region_soup = BeautifulSoup(region_content, 'html.parser')
    
    # Find the Bradford city card
    city_cards = region_soup.find_all('div', class_='city-card')
    for card in city_cards:
        city_name = card.find('h3')
        if city_name and old_city_name in city_name.text:
            # Update the city name
            city_name.string = new_city_name
            
            # Update the link
            link = card.find('a')
            if link:
                link['href'] = f"selfstorage{new_normalized}/index.html"
                
            # The count should remain the same as it's the same number of facilities
            print(f"Updated West Yorkshire region page for Bradford")
            break
    
    # Save the region page
    with open(region_html, 'w', encoding='utf-8') as f:
        f.write(str(region_soup))

if __name__ == "__main__":
    update_bradford() 