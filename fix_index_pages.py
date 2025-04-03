import os
import re
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor

def find_index_pages():
    """Find all index.html files at the region level"""
    index_pages = []
    website_dir = os.path.join(os.getcwd(), "website")
    
    for root, dirs, files in os.walk(website_dir):
        if "index.html" in files:
            # Check if this is a region-level index.html (not a city page)
            # Region pages are typically one level deep: website/selfstorage{region}/index.html
            rel_path = os.path.relpath(root, website_dir)
            if rel_path == "." or (rel_path.startswith("selfstorage") and "/" not in rel_path.replace("\\", "/")):
                index_pages.append(os.path.join(root, "index.html"))
    
    return index_pages

def clean_region_name(region_name):
    """Clean the region name for display purposes"""
    if not region_name:
        return "UK"
    
    # Remove 'selfstorage' prefix if present
    if region_name.startswith("selfstorage"):
        region_name = region_name[11:]
    
    # Replace hyphens with spaces and capitalize words
    region_name = region_name.replace("-", " ").strip()
    
    # Handle special cases
    if region_name.lower() == "uk":
        return "the UK"
    
    return region_name.title()

def get_region_cities(region_path):
    """Get a list of cities in the region for creating links"""
    cities = []
    region_dir = os.path.dirname(region_path)
    
    for item in os.listdir(region_dir):
        item_path = os.path.join(region_dir, item)
        if os.path.isdir(item_path) and "index.html" in os.listdir(item_path):
            city_name = item
            if city_name.startswith("selfstorage"):
                city_name = city_name[11:]
            city_name = city_name.replace("-", " ").title()
            cities.append({
                "name": city_name,
                "path": os.path.join(item, "index.html")
            })
    
    return cities[:6]  # Return up to 6 cities for the list

def update_main_homepage(filepath):
    """Update the main homepage with proper content"""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    
    # Update meta description if needed
    meta_desc = soup.find("meta", {"name": "description"})
    if not meta_desc or "placeholder" in meta_desc.get("content", "").lower():
        if not meta_desc:
            meta_desc = soup.new_tag("meta")
            meta_desc["name"] = "description"
            head = soup.find("head")
            if head:
                head.append(meta_desc)
        
        meta_desc["content"] = "Find the best self storage facilities across the UK. Compare prices, services, and features to get the perfect storage solution for your needs."
    
    # Update main content
    main_content = soup.find("main")
    if main_content and "placeholder" in main_content.text.lower():
        # Create new content for the homepage
        main_content.clear()
        
        # Hero section
        hero = soup.new_tag("section")
        hero["class"] = "hero"
        
        hero_title = soup.new_tag("h1")
        hero_title.string = "Find Self Storage Facilities Near You"
        hero.append(hero_title)
        
        hero_desc = soup.new_tag("p")
        hero_desc.string = "Compare the best self storage solutions across the UK. Get quotes, check availability, and book online today."
        hero.append(hero_desc)
        
        main_content.append(hero)
        
        # Popular regions section
        popular_regions = soup.new_tag("section")
        popular_regions["class"] = "popular-regions"
        
        regions_title = soup.new_tag("h2")
        regions_title.string = "Popular Storage Regions"
        popular_regions.append(regions_title)
        
        regions_list = soup.new_tag("div")
        regions_list["class"] = "regions-grid"
        
        top_regions = [
            "Greater London", "West Midlands", "Greater Manchester", 
            "West Yorkshire", "Glasgow City", "Merseyside"
        ]
        
        for region in top_regions:
            region_slug = "selfstorage" + region.lower().replace(" ", "-")
            
            region_card = soup.new_tag("div")
            region_card["class"] = "region-card"
            
            region_link = soup.new_tag("a")
            region_link["href"] = f"{region_slug}/index.html"
            region_link.string = f"Self Storage in {region}"
            
            region_card.append(region_link)
            regions_list.append(region_card)
        
        popular_regions.append(regions_list)
        main_content.append(popular_regions)
        
        # Features section
        features = soup.new_tag("section")
        features["class"] = "features"
        
        features_title = soup.new_tag("h2")
        features_title.string = "Why Choose Our Self Storage Comparison"
        features.append(features_title)
        
        features_grid = soup.new_tag("div")
        features_grid["class"] = "features-grid"
        
        feature_items = [
            {"title": "Best Prices Guaranteed", "desc": "We compare prices across all major providers to ensure you get the best deal."},
            {"title": "Thousands of Locations", "desc": "With facilities across the UK, you'll always find storage near you."},
            {"title": "Secure Facilities", "desc": "All storage facilities meet our high security standards for your peace of mind."},
            {"title": "Flexible Options", "desc": "From personal storage to business solutions, find the perfect space for your needs."}
        ]
        
        for item in feature_items:
            feature = soup.new_tag("div")
            feature["class"] = "feature"
            
            feature_title = soup.new_tag("h3")
            feature_title.string = item["title"]
            feature.append(feature_title)
            
            feature_desc = soup.new_tag("p")
            feature_desc.string = item["desc"]
            feature.append(feature_desc)
            
            features_grid.append(feature)
        
        features.append(features_grid)
        main_content.append(features)
    
    # Write the updated content back to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    return True

def update_region_page(filepath):
    """Update a region index page with proper content and storage list"""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    
    # Get the region name from the filepath
    region_path = os.path.dirname(filepath)
    region_folder = os.path.basename(region_path)
    region_name = clean_region_name(region_folder)
    
    # Update the title if needed
    title_tag = soup.find("title")
    if title_tag and ("placeholder" in title_tag.text.lower() or title_tag.text.strip() == ""):
        title_tag.string = f"Self Storage in {region_name} - Compare Facilities"
    
    # Update meta description if needed
    meta_desc = soup.find("meta", {"name": "description"})
    if not meta_desc or "placeholder" in meta_desc.get("content", "").lower():
        if not meta_desc:
            meta_desc = soup.new_tag("meta")
            meta_desc["name"] = "description"
            head = soup.find("head")
            if head:
                head.append(meta_desc)
        
        meta_desc["content"] = f"Find the best self storage facilities in {region_name}. Compare prices, locations, and services to get the perfect storage solution in your area."
    
    # Update main content and add storage-list if missing
    main_content = soup.find("main")
    if main_content and ("placeholder" in main_content.text.lower() or not main_content.find(class_="storage-list")):
        # Clear current content if it has placeholder text
        if "placeholder" in main_content.text.lower():
            main_content.clear()
        
        # Add or update the heading
        h1 = main_content.find("h1")
        if not h1:
            h1 = soup.new_tag("h1")
            main_content.append(h1)
        h1.string = f"Self Storage in {region_name}"
        
        # Add introduction paragraph if not present
        intro = main_content.find("p", class_="intro")
        if not intro:
            intro = soup.new_tag("p")
            intro["class"] = "intro"
            main_content.append(intro)
        intro.string = f"Looking for self storage in {region_name}? Compare the best storage facilities in the region. Find secure, affordable storage units for personal or business use."
        
        # Add breadcrumbs navigation
        breadcrumbs = main_content.find(class_="breadcrumbs")
        if not breadcrumbs:
            breadcrumbs = soup.new_tag("div")
            breadcrumbs["class"] = "breadcrumbs"
            
            home_link = soup.new_tag("a")
            home_link["href"] = "/index.html"
            home_link.string = "Home"
            
            separator = soup.new_tag("span")
            separator.string = " > "
            
            current = soup.new_tag("span")
            current.string = f"{region_name}"
            
            breadcrumbs.append(home_link)
            breadcrumbs.append(separator)
            breadcrumbs.append(current)
            
            # Insert after h1
            h1.insert_after(breadcrumbs)
        
        # Add or update the storage-list container
        storage_list = main_content.find(class_="storage-list")
        if not storage_list:
            storage_list = soup.new_tag("div")
            storage_list["class"] = "storage-list"
            main_content.append(storage_list)
        else:
            storage_list.clear()
        
        # Get cities in this region
        cities = get_region_cities(filepath)
        
        # Add section title
        section_title = soup.new_tag("h2")
        section_title.string = f"Cities with Storage Facilities in {region_name}"
        storage_list.append(section_title)
        
        # Create grid of city cards
        city_grid = soup.new_tag("div")
        city_grid["class"] = "storage-grid"
        
        for city in cities:
            city_card = soup.new_tag("div")
            city_card["class"] = "storage-card"
            
            city_link = soup.new_tag("a")
            city_link["href"] = city["path"]
            city_link.string = f"Self Storage in {city['name']}"
            
            city_card.append(city_link)
            city_grid.append(city_card)
        
        storage_list.append(city_grid)
        
        # Add additional info section
        info_section = soup.new_tag("section")
        info_section["class"] = "region-info"
        
        info_title = soup.new_tag("h2")
        info_title.string = f"About Self Storage in {region_name}"
        info_section.append(info_title)
        
        info_text = soup.new_tag("p")
        info_text.string = f"Self storage facilities in {region_name} offer a range of unit sizes and features to meet your storage needs. Whether you're moving home, storing business inventory, or need extra space for personal belongings, you'll find secure, accessible storage solutions throughout the region."
        info_section.append(info_text)
        
        main_content.append(info_section)
    
    # Write the updated content back to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    return True

def main():
    start_time = time.time()
    
    # Find all index.html files
    print("Finding index pages...")
    index_pages = find_index_pages()
    print(f"Found {len(index_pages)} index pages.")
    
    updated_count = 0
    error_count = 0
    
    # Process the main homepage separately
    main_homepage = os.path.join(os.getcwd(), "website", "index.html")
    if os.path.exists(main_homepage):
        print(f"Updating main homepage: {main_homepage}")
        try:
            if update_main_homepage(main_homepage):
                updated_count += 1
                print(f"[{updated_count}/{len(index_pages)}] Updated: {main_homepage}")
        except Exception as e:
            error_count += 1
            print(f"Error updating {main_homepage}: {str(e)}")
    
    # Process region index pages with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        
        for page in index_pages:
            if page != main_homepage:  # Skip the main homepage as it's already processed
                futures.append(executor.submit(update_region_page, page))
        
        for i, future in enumerate(futures):
            try:
                if future.result():
                    updated_count += 1
                    print(f"[{updated_count}/{len(index_pages)}] Updated: {index_pages[i+1] if i+1 < len(index_pages) else 'unknown'}")
            except Exception as e:
                error_count += 1
                print(f"Error updating {index_pages[i+1] if i+1 < len(index_pages) else 'unknown'}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\nUpdate summary:")
    print(f"- Total index pages: {len(index_pages)}")
    print(f"- Successfully updated: {updated_count}")
    print(f"- Errors: {error_count}")
    print(f"- Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main() 