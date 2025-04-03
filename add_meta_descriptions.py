import os
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def find_all_html_files():
    """Find all HTML files in the website directory."""
    html_files = []
    
    for root, dirs, files in os.walk('website'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    return html_files

def clean_name(name):
    """Clean a region or city name from a directory path."""
    if name.startswith('selfstorage'):
        name = name[len('selfstorage'):]
    
    # Replace hyphens with spaces and title case
    name = name.replace('-', ' ').title()
    
    return name

def add_meta_description(filepath):
    """Add or update meta description on an HTML page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if meta description already exists
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content') and len(meta_desc.get('content', '').strip()) >= 50:
            # Already has a good meta description
            return {'filepath': filepath, 'status': 'skipped', 'message': 'Already has meta description'}
        
        # Determine page type and content based on filepath
        parts = filepath.split(os.sep)
        page_type = 'unknown'
        region_name = ''
        city_name = ''
        
        if len(parts) >= 3:
            if parts[-1] == 'index.html':
                if parts[-2] == 'website':
                    page_type = 'homepage'
                elif parts[-2] == 'about':
                    page_type = 'about'
                elif parts[-2] == 'contact':
                    page_type = 'contact'
                elif parts[-2] == 'membership':
                    page_type = 'membership'
                elif parts[-2] == 'terms':
                    page_type = 'terms'
                elif parts[-2] == 'privacy':
                    page_type = 'privacy'
                elif parts[-2] == 'selfstorageregions':
                    page_type = 'regions'
                elif parts[-2].startswith('selfstorage') and len(parts) == 3:
                    # It's a region page (e.g. website/selfstoragebedfordshire/index.html)
                    page_type = 'region'
                    region_name = clean_name(parts[-2])
                elif parts[-2].startswith('selfstorage') and len(parts) > 3:
                    # It's a city page (e.g. website/selfstoragebedfordshire/selfstoragebedford/index.html)
                    page_type = 'city'
                    city_name = clean_name(parts[-2])
                    region_name = clean_name(parts[-3])
        
        # Create meta description based on page type
        description = ""
        
        if page_type == 'homepage':
            description = "Find the best self storage facilities near you. Compare prices, features, and availability of storage units across the UK. Our comprehensive directory helps you find the perfect storage solution."
        elif page_type == 'about':
            description = "Learn about our mission to help you find the best self storage solutions in the UK. Our comprehensive directory connects you with storage facilities that meet your needs and budget."
        elif page_type == 'contact':
            description = "Contact us for help finding the perfect self storage solution in your area. Our team is ready to assist you with any questions about storage facilities across the UK."
        elif page_type == 'membership':
            description = "Join our storage providers membership program and get your facility listed in our UK-wide directory. Increase visibility and connect with customers looking for storage solutions."
        elif page_type == 'terms':
            description = "Our terms and conditions for using the UK's most comprehensive self storage facilities directory. Find information about our service agreements and user responsibilities."
        elif page_type == 'privacy':
            description = "Our privacy policy outlines how we protect your data when using our self storage facilities directory. Learn how we safeguard your personal information when you use our services."
        elif page_type == 'regions':
            description = "Browse self storage facilities across all UK regions. Our directory helps you find secure storage solutions no matter where you're located in the United Kingdom."
        elif page_type == 'region' and region_name:
            description = f"Find the best self storage facilities in {region_name}. Compare prices, features, and availability of storage units near you throughout the {region_name} area."
        elif page_type == 'city' and city_name and region_name:
            description = f"Looking for self storage in {city_name}, {region_name}? Compare local storage facilities, prices, and features to find the perfect storage solution for your needs."
        else:
            description = "Find the perfect self storage facility near you. Our UK-wide directory helps you compare storage units, prices, and features to meet your personal or business storage needs."
        
        # Add or update meta description
        if meta_desc:
            meta_desc['content'] = description
        else:
            # Create new meta tag
            meta_desc = soup.new_tag('meta')
            meta_desc['name'] = 'description'
            meta_desc['content'] = description
            
            # Add it to head
            head = soup.head
            if head:
                # Add after title if it exists
                title = head.find('title')
                if title:
                    title.insert_after(meta_desc)
                else:
                    head.append(meta_desc)
            else:
                # If no head, create it
                head = soup.new_tag('head')
                head.append(meta_desc)
                if soup.html:
                    soup.html.insert(0, head)
                else:
                    soup.insert(0, head)
        
        # Write the updated HTML back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return {'filepath': filepath, 'status': 'updated', 'message': f"Added meta description for {page_type} page"}
    
    except Exception as e:
        return {'filepath': filepath, 'status': 'error', 'message': str(e)}

def main():
    """Add meta descriptions to all HTML pages in the website."""
    print("Finding all HTML files...")
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files.")
    
    print("Adding meta descriptions...")
    
    start_time = time.time()
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(add_meta_description, filepath): filepath for filepath in html_files}
        
        for i, future in enumerate(as_completed(future_to_file)):
            filepath = future_to_file[future]
            
            try:
                result = future.result()
                
                if result['status'] == 'updated':
                    updated_count += 1
                    print(f"[{i+1}/{len(html_files)}] Updated: {filepath}")
                elif result['status'] == 'skipped':
                    skipped_count += 1
                    if i % 50 == 0:  # Only show some of the skipped files to reduce output
                        print(f"[{i+1}/{len(html_files)}] Skipped: {filepath}")
                else:
                    error_count += 1
                    print(f"[{i+1}/{len(html_files)}] Error: {filepath} - {result['message']}")
            
            except Exception as e:
                error_count += 1
                print(f"[{i+1}/{len(html_files)}] Error: {filepath} - {e}")
    
    elapsed_time = time.time() - start_time
    
    print("\nUpdate summary:")
    print(f"- Total HTML files: {len(html_files)}")
    print(f"- Updated with meta descriptions: {updated_count}")
    print(f"- Skipped (already had good meta descriptions): {skipped_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 