import pandas as pd
from bs4 import BeautifulSoup

def update_aberdeen_page():
    """Update the Aberdeen city page with data from Excel."""
    # Path to the Excel file and HTML file
    excel_file = 'self storage facilities uk.xlsx'
    aberdeen_html = 'website/selfstorageaberdeen-city/selfstorageaberdeen/index.html'
    
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Filter for Aberdeen entries
    aberdeen_df = df[(df['CITY'].str.strip() == 'Aberdeen') & 
                     (df['Region'].str.strip() == 'Aberdeen City')]
    
    # Read the HTML file
    with open(aberdeen_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the storage-list div
    storage_list = soup.find('div', class_='storage-list')
    if not storage_list:
        print("Storage list not found in Aberdeen HTML file")
        return
    
    # Clear existing storage cards
    storage_list.clear()
    
    # Process each facility from Excel
    for _, row in aberdeen_df.iterrows():
        # Extract facility data
        name = str(row.get('Name of Self Storage', '')).strip()
        website = str(row.get('Website', '')).strip().replace('https://', '').replace('http://', '')
        email = str(row.get('Email / Contact', '')).strip()
        phone = str(row.get('Telephone Number', '')).strip()
        address = str(row.get('Location', '')).strip()
        
        # Skip if essential data is missing
        if not name or not address:
            continue
        
        # Create description
        description = f"{name} provides self storage solutions in Aberdeen, Aberdeen City. Located at {address} with easy access and secure storage options."
        
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
        if phone:
            phone_p = soup.new_tag('p')
            phone_strong = soup.new_tag('strong')
            phone_strong.string = 'Phone: '
            phone_p.append(phone_strong)
            
            phone_link = soup.new_tag('a', href=f"tel:{phone.replace(' ', '')}")
            phone_link.string = phone
            phone_p.append(phone_link)
            contact.append(phone_p)
        
        # Add website
        if website:
            website_p = soup.new_tag('p')
            website_strong = soup.new_tag('strong')
            website_strong.string = 'Website: '
            website_p.append(website_strong)
            
            website_link = soup.new_tag('a', href=f"https://{website}", target="_blank")
            website_link.string = website
            website_p.append(website_link)
            contact.append(website_p)
        
        # Add email
        if email and email != 'nan':
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
    with open(aberdeen_html, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Successfully updated Aberdeen page with {len(aberdeen_df)} facilities")

    # Now update the region page
    region_html = 'website/selfstorageaberdeen-city/index.html'
    
    with open(region_html, 'r', encoding='utf-8') as f:
        region_content = f.read()
    
    region_soup = BeautifulSoup(region_content, 'html.parser')
    
    # Find the Aberdeen city card
    city_cards = region_soup.find_all('div', class_='city-card')
    for card in city_cards:
        city_name = card.find('h3').text.lower()
        if 'aberdeen' in city_name:
            # Update the count
            p_tag = card.find('p')
            if p_tag:
                facilities_count = len(aberdeen_df)
                facility_text = f"{facilities_count} Storage {'Facilities' if facilities_count != 1 else 'Facility'}"
                p_tag.string = facility_text
                print(f"Updated region page with '{facility_text}' for Aberdeen")
    
    # Save the region page
    with open(region_html, 'w', encoding='utf-8') as f:
        f.write(str(region_soup))

if __name__ == "__main__":
    update_aberdeen_page() 