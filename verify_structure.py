import os

def check_website_structure():
    """Check the current website structure and report what was found"""
    print("Verifying website structure...")
    
    root_path = 'website'
    if not os.path.exists(root_path):
        print(f"ERROR: Website directory {root_path} does not exist!")
        return
    
    # Check for homepage
    homepage_path = os.path.join(root_path, 'index.html')
    if os.path.exists(homepage_path):
        print(f"✓ Homepage exists: {homepage_path}")
    else:
        print(f"✗ Homepage missing: {homepage_path}")
    
    # Check for top-level folders
    top_level_folders = ['about', 'faq', 'contact', 'privacy', 'terms', 'membership', 'selfstorageregions']
    found_folders = []
    missing_folders = []
    
    for folder in top_level_folders:
        folder_path = os.path.join(root_path, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            found_folders.append(folder)
            # Check for index.html in folder
            index_path = os.path.join(folder_path, 'index.html')
            if os.path.exists(index_path):
                print(f"✓ Found {folder}/index.html")
            else:
                print(f"✗ Missing {folder}/index.html")
        else:
            missing_folders.append(folder)
    
    if missing_folders:
        print(f"✗ Missing top-level folders: {', '.join(missing_folders)}")
    else:
        print("✓ All top-level folders found.")
    
    # Check for region folders (selfstorage*)
    region_folders = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path) and item.startswith('selfstorage') and item != 'selfstorageregions':
            region_folders.append(item)
    
    if region_folders:
        print(f"✓ Found {len(region_folders)} region folders")
        for region in region_folders[:5]:  # Show first 5 only
            print(f"  - {region}")
        if len(region_folders) > 5:
            print(f"  ... and {len(region_folders) - 5} more")
        
        # Check a sample region for city folders
        if region_folders:
            sample_region = region_folders[0]
            sample_path = os.path.join(root_path, sample_region)
            city_folders = []
            for item in os.listdir(sample_path):
                item_path = os.path.join(sample_path, item)
                if os.path.isdir(item_path):
                    city_folders.append(item)
            
            if city_folders:
                print(f"✓ Found {len(city_folders)} city folders in {sample_region}")
                for city in city_folders[:3]:  # Show first 3 only
                    print(f"  - {city}")
                if len(city_folders) > 3:
                    print(f"  ... and {len(city_folders) - 3} more")
            else:
                print(f"✗ No city folders found in {sample_region}")
    else:
        print("✗ No region folders (selfstorage*) found!")
    
    # Check assets folder
    assets_path = os.path.join(root_path, 'assets')
    if os.path.exists(assets_path) and os.path.isdir(assets_path):
        print("✓ Assets folder found")
        # Check for CSS and JS folders
        css_path = os.path.join(assets_path, 'css')
        js_path = os.path.join(assets_path, 'js')
        
        if os.path.exists(css_path) and os.path.isdir(css_path):
            print("  ✓ CSS folder found")
        else:
            print("  ✗ CSS folder missing")
        
        if os.path.exists(js_path) and os.path.isdir(js_path):
            print("  ✓ JS folder found")
        else:
            print("  ✗ JS folder missing")
    else:
        print("✗ Assets folder missing")
    
    print("Structure verification completed.")

if __name__ == "__main__":
    check_website_structure() 