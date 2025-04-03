import os
import pandas as pd
import re
import shutil
from pathlib import Path
import unicodedata

def create_basic_structure():
    """Create the basic website structure with necessary folders"""
    print("Creating basic website structure...")
    
    root_path = 'website'
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    # Create top-level directories
    for folder in ['about', 'faq', 'contact', 'privacy', 'terms', 'membership', 'selfstorageregions']:
        folder_path = os.path.join(root_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Create index.html file
        index_path = os.path.join(folder_path, 'index.html')
        with open(index_path, 'w') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{folder.capitalize()} - Self Storage Near Me</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header>
        <div class="logo">Storage Finder</div>
        <nav>
            <ul>
                <li><a href="../index.html">Home</a></li>
                <li><a href="../selfstorageregions/index.html">Regions</a></li>
                <li><a href="../faq/index.html">FAQ</a></li>
                <li><a href="../about/index.html">About</a></li>
                <li><a href="../contact/index.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h1>{folder.capitalize()} Page</h1>
        <p>This is the {folder} page content.</p>
    </main>
    <footer>
        <p>&copy; 2023 Self Storage Finder. All rights reserved.</p>
        <ul>
            <li><a href="../privacy/index.html">Privacy Policy</a></li>
            <li><a href="../terms/index.html">Terms of Use</a></li>
        </ul>
    </footer>
</body>
</html>""")
    
    # Create assets directory and subdirectories
    assets_path = os.path.join(root_path, 'assets')
    css_path = os.path.join(assets_path, 'css')
    js_path = os.path.join(assets_path, 'js')
    
    for path in [assets_path, css_path, js_path]:
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Create a basic CSS file
    css_file = os.path.join(css_path, 'style.css')
    with open(css_file, 'w') as f:
        f.write("""body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
}

header {
    background-color: #333;
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav ul {
    display: flex;
    list-style: none;
}

nav ul li {
    margin-left: 1rem;
}

nav ul li a {
    color: white;
    text-decoration: none;
}

main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    text-align: center;
}

footer ul {
    display: flex;
    justify-content: center;
    list-style: none;
}

footer ul li {
    margin: 0 1rem;
}

footer ul li a {
    color: white;
    text-decoration: none;
}
""")
    
    # Create a basic homepage
    homepage_path = os.path.join(root_path, 'index.html')
    with open(homepage_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage Near Me | Find Local Storage Facilities</title>
    <meta name="description" content="Find the best self storage facilities near you. Compare prices, amenities, and book online.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="logo">Storage Finder</div>
        <nav>
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="selfstorageregions/index.html">Regions</a></li>
                <li><a href="faq/index.html">FAQ</a></li>
                <li><a href="about/index.html">About</a></li>
                <li><a href="contact/index.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="hero">
            <h1>Find Self Storage Near You</h1>
            <p>Compare storage facilities and find the best deal for your needs.</p>
            <form action="results.html" method="get">
                <input type="text" name="location" placeholder="Enter your location">
                <button type="submit">Search</button>
            </form>
        </section>
        
        <section class="popular-regions">
            <h2>Popular Storage Regions</h2>
            <div class="regions-grid">
                <div class="region-card">
                    <h3>Devon</h3>
                    <p>23 cities, 45 facilities</p>
                    <a href="selfstoragedevon/index.html" class="btn">View Region</a>
                </div>
                <!-- More region cards would go here -->
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2023 Self Storage Finder. All rights reserved.</p>
        <ul>
            <li><a href="privacy/index.html">Privacy Policy</a></li>
            <li><a href="terms/index.html">Terms of Use</a></li>
        </ul>
    </footer>
</body>
</html>""")
    
    print("Basic website structure created successfully!")

def clean_text(text):
    """Clean text by removing Unicode characters and trimming whitespace"""
    # Convert to string if not already
    text = str(text)
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Replace any remaining problematic characters with ordinary ASCII equivalents
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Remove any special characters like ‎ (left-to-right mark)
    text = re.sub(r'[\u200e\u200f\u202a-\u202e]', '', text)
    
    # Remove common suffixes like "‎" that might appear in Excel data
    text = re.sub(r'[,\s]+$', '', text)
    
    # Remove commas and any text after them (like "Sandy, Bedfordshire‎" → "Sandy")
    if ',' in text:
        text = text.split(',')[0].strip()
    
    return text.strip()

def create_regions_from_excel():
    """Create region and city folders based on the Excel file data"""
    print("Creating regions and cities from Excel data...")
    
    excel_path = 'self storage facilities uk.xlsx'
    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found: {excel_path}")
        return
    
    # Read the Excel file
    try:
        df = pd.read_excel(excel_path)
        print(f"Successfully read Excel file with {len(df)} rows")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return
    
    # Create region and city folders
    root_path = 'website'
    regions = {}
    
    for _, row in df.iterrows():
        # Use the correct column names from the Excel file and clean the text
        region = clean_text(row['Region'])
        city = clean_text(row['CITY'])
        
        if not region or not city:
            continue  # Skip empty values
        
        if region not in regions:
            regions[region] = []
        
        if city not in regions[region]:
            regions[region].append(city)
    
    print(f"Found {len(regions)} unique regions")
    
    # Process each region and its cities
    for region, cities in regions.items():
        region_name = to_selfstorage_path(region)
        region_path = os.path.join(root_path, region_name)
        
        if not os.path.exists(region_path):
            os.makedirs(region_path)
        
        # Create region index.html
        create_region_page(region_path, region, cities)
        
        # Create city folders and their index.html files
        for city in cities:
            city_name = to_selfstorage_path(city)
            city_path = os.path.join(region_path, city_name)
            
            if not os.path.exists(city_path):
                os.makedirs(city_path)
            
            # Create city index.html
            create_city_page(city_path, region, city)
    
    # Create regions index page
    create_regions_index(root_path, regions)
    
    print("Regions and cities created successfully!")

def to_selfstorage_path(name):
    """Convert a name to a valid folder name with selfstorage prefix"""
    # Skip if already has prefix
    if str(name).startswith('selfstorage'):
        return str(name)
    
    # Convert name to lowercase with dashes
    name = re.sub(r'[^a-zA-Z0-9]', '-', str(name)).lower()
    return 'selfstorage' + name

def create_region_page(region_path, region_name, cities):
    """Create an index.html file for a region"""
    index_path = os.path.join(region_path, 'index.html')
    
    with open(index_path, 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage in {region_name} | Find Local Storage Facilities</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header>
        <div class="logo">Storage Finder</div>
        <nav>
            <ul>
                <li><a href="../index.html">Home</a></li>
                <li><a href="../selfstorageregions/index.html">Regions</a></li>
                <li><a href="../faq/index.html">FAQ</a></li>
                <li><a href="../about/index.html">About</a></li>
                <li><a href="../contact/index.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h1>Self Storage in {region_name}</h1>
        <p>Find the best self storage facilities in {region_name}. We have {len(cities)} locations available.</p>
        
        <h2>Cities in {region_name}</h2>
        <ul>
""")
        
        # Add links to each city
        for city in cities:
            city_folder = to_selfstorage_path(city)
            f.write(f'            <li><a href="{city_folder}/index.html">{city}</a></li>\n')
        
        f.write("""        </ul>
    </main>
    <footer>
        <p>&copy; 2023 Self Storage Finder. All rights reserved.</p>
        <ul>
            <li><a href="../privacy/index.html">Privacy Policy</a></li>
            <li><a href="../terms/index.html">Terms of Use</a></li>
        </ul>
    </footer>
</body>
</html>""")

def create_city_page(city_path, region_name, city_name):
    """Create an index.html file for a city"""
    index_path = os.path.join(city_path, 'index.html')
    region_folder = to_selfstorage_path(region_name)
    
    with open(index_path, 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage in {city_name}, {region_name} | Find Local Facilities</title>
    <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
    <header>
        <div class="logo">Storage Finder</div>
        <nav>
            <ul>
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../../selfstorageregions/index.html">Regions</a></li>
                <li><a href="../../faq/index.html">FAQ</a></li>
                <li><a href="../../about/index.html">About</a></li>
                <li><a href="../../contact/index.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h1>Self Storage in {city_name}, {region_name}</h1>
        <p>Find the best self storage facilities in {city_name}, {region_name}.</p>
        
        <div class="breadcrumbs">
            <a href="../../index.html">Home</a> &gt;
            <a href="../../selfstorageregions/index.html">Regions</a> &gt;
            <a href="../index.html">{region_name}</a> &gt;
            <span>{city_name}</span>
        </div>
        
        <h2>Storage Providers in {city_name}</h2>
        <div class="provider-list">
            <div class="provider">
                <h3>ABC Storage</h3>
                <p>123 Main St, {city_name}, {region_name}</p>
                <p>Phone: 123-456-7890</p>
                <p>Website: <a href="https://example.com">www.example.com</a></p>
            </div>
            <div class="provider">
                <h3>XYZ Storage Solutions</h3>
                <p>456 Oak Ave, {city_name}, {region_name}</p>
                <p>Phone: 987-654-3210</p>
                <p>Website: <a href="https://example.org">www.example.org</a></p>
            </div>
        </div>
    </main>
    <footer>
        <p>&copy; 2023 Self Storage Finder. All rights reserved.</p>
        <ul>
            <li><a href="../../privacy/index.html">Privacy Policy</a></li>
            <li><a href="../../terms/index.html">Terms of Use</a></li>
        </ul>
    </footer>
</body>
</html>""")

def create_regions_index(root_path, regions):
    """Create the main regions index page"""
    regions_path = os.path.join(root_path, 'selfstorageregions', 'index.html')
    
    with open(regions_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage Regions | Find Local Storage Facilities</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header>
        <div class="logo">Storage Finder</div>
        <nav>
            <ul>
                <li><a href="../index.html">Home</a></li>
                <li><a href="../selfstorageregions/index.html">Regions</a></li>
                <li><a href="../faq/index.html">FAQ</a></li>
                <li><a href="../about/index.html">About</a></li>
                <li><a href="../contact/index.html">Contact</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <h1>Self Storage Regions</h1>
        <p>Browse self storage facilities by region.</p>
        
        <div class="regions-list">
""")
        
        # Add links to each region
        for region, cities in regions.items():
            region_folder = to_selfstorage_path(region)
            f.write(f"""            <div class="region-card">
                <h2>{region}</h2>
                <p>{len(cities)} cities available</p>
                <a href="../{region_folder}/index.html" class="btn">View Region</a>
            </div>
""")
        
        f.write("""        </div>
    </main>
    <footer>
        <p>&copy; 2023 Self Storage Finder. All rights reserved.</p>
        <ul>
            <li><a href="../privacy/index.html">Privacy Policy</a></li>
            <li><a href="../terms/index.html">Terms of Use</a></li>
        </ul>
    </footer>
</body>
</html>""")

def main():
    """Main function to execute the script"""
    # Step 1: Create the basic website structure
    create_basic_structure()
    
    # Step 2: Create region and city folders from Excel data
    create_regions_from_excel()
    
    print("Website structure has been fixed successfully!")

if __name__ == "__main__":
    main() 