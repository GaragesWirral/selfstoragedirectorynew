import pandas as pd
import os
import re
from collections import defaultdict

# Function to generate facility cards with modern styling
def generate_facility_card(facility):
    facility_name = facility['name']
    location = facility.get('location', 'Address not available').replace('\n', '<br>')
    phone = facility.get('phone', 'Not available')
    email = facility.get('email', 'Not available')
    website = facility.get('website', '')
    
    website_display = ''
    if website and website != 'Not available':
        website_display = f'<p><strong>Website:</strong> {website}</p>'
    
    return f"""
            <div class="storage-card">
                <h3>{facility_name}</h3>
                <div class="storage-info">
                    <p><strong>Location:</strong> {location}</p>
                </div>
                <div class="contact-info">
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Email:</strong> {email}</p>
                    {website_display}
                </div>
            </div>"""

# Create the website directory
website_dir = 'website'
os.makedirs(website_dir, exist_ok=True)

# Read the Excel file
df = pd.read_excel('self storage facilities uk.xlsx')

# Basic stats
print(f"Total records: {len(df)}")
print(f"Unique regions: {df['Region'].nunique()}")
print(f"Unique cities: {df['CITY'].nunique()}")

# Create directories
if not os.path.exists('website'):
    os.makedirs('website')
    os.makedirs('website/assets')
    os.makedirs('website/assets/css')
    os.makedirs('website/assets/js')

# Create CSS file
css_content = """/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

/* General Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Roboto', sans-serif;
}

body {
    background-color: #F8F9FA;
    color: #333333;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    font-size: 32px;
    margin-bottom: 15px;
    font-weight: 700;
}

h2 {
    font-size: 24px;
    margin-bottom: 15px;
    font-weight: 700;
}

h3 {
    font-size: 20px;
    margin-bottom: 15px;
    font-weight: 700;
}

p {
    font-size: 16px;
    margin-bottom: 15px;
}

/* Header Styles */
header {
    background-color: #006400;
    color: white;
    padding: 15px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

nav ul {
    display: flex;
    list-style: none;
}

nav ul li {
    margin-left: 20px;
}

nav ul li a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}

nav ul li a:hover {
    opacity: 0.8;
}

/* Hero Section */
.hero {
    background-color: #F8F9FA;
    padding: 50px 0;
    text-align: center;
    margin-bottom: 40px;
    border-bottom: 1px solid #e9ecef;
}

.hero h1 {
    font-size: 36px;
    margin-bottom: 20px;
}

.hero p {
    font-size: 18px;
    max-width: 800px;
    margin: 0 auto 30px;
}

/* Button Styles */
.btn {
    display: inline-block;
    background-color: #28A745;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #218838;
}

/* Search Form */
.search-form {
    margin-bottom: 30px;
    text-align: center;
}

.search-form input {
    padding: 12px;
    width: 300px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    font-size: 16px;
}

.search-form select {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 0 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    font-size: 16px;
}

.search-form button {
    padding: 12px 25px;
    background-color: #28A745;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.3s;
    font-size: 16px;
}

.search-form button:hover {
    background-color: #218838;
}

/* Regions List */
.regions-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}

/* Region Card */
.region-card {
    background-color: white;
    border: 1px solid #28A745;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.region-card:hover {
    transform: scale(1.05);
}

.region-card h3 {
    color: #333333;
    margin-bottom: 10px;
}

.region-card p {
    margin-bottom: 15px;
    color: #666;
}

.region-card .btn {
    display: block;
    text-align: center;
}

.region-card ul {
    list-style: none;
    padding-left: 10px;
}

.region-card ul li {
    margin-bottom: 5px;
}

.region-card ul li a {
    color: #006400;
    text-decoration: none;
}

/* Storage List */
.storage-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 30px;
}

/* Storage Card */
.storage-card {
    background-color: white;
    border: 1px solid #28A745;
    border-radius: 5px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.storage-card h3 {
    color: #333333;
    margin-bottom: 10px;
}

.storage-info {
    margin-bottom: 15px;
}

.contact-info a {
    color: #006400;
    text-decoration: none;
    transition: color 0.3s;
}

.contact-info a:hover {
    color: #004d00;
}

/* Footer */
footer {
    background-color: #006400;
    color: white;
    padding: 40px 0 20px;
    margin-top: 40px;
}

.footer-columns {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 30px;
    margin-bottom: 20px;
}

.footer-column h3 {
    font-size: 18px;
    margin-bottom: 15px;
    color: #fff;
}

.footer-column ul {
    list-style: none;
    padding: 0;
}

.footer-column ul li {
    margin-bottom: 8px;
}

.footer-column ul li a {
    color: #adb5bd;
    text-decoration: none;
    transition: color 0.2s;
}

.footer-column ul li a:hover {
    color: #fff;
}

.footer-bottom {
    border-top: 1px solid #495057;
    padding-top: 20px;
    text-align: center;
}

/* Responsive Styles */
@media (max-width: 768px) {
    .regions-list {
        grid-template-columns: 1fr;
    }
    
    header .container {
        flex-direction: column;
    }
    
    nav ul {
        margin-top: 15px;
    }
    
    .footer-columns {
        flex-direction: column;
        gap: 20px;
    }
    
    .search-form input,
    .search-form select {
        width: 100%;
        margin-bottom: 10px;
    }
    
    .search-form button {
        width: 100%;
    }
}
"""

with open('website/assets/css/style.css', 'w') as f:
    f.write(css_content)

# Organize data by region and city
region_data = defaultdict(lambda: defaultdict(list))

for _, row in df.iterrows():
    region = row['Region']
    city = row['CITY'].strip()
    
    if pd.isna(city) or city == '':
        continue
        
    # Clean city name for URL
    city_clean = re.sub(r'[^\w\s-]', '', city).strip()
    city_clean = re.sub(r'\s+', '-', city_clean)
    
    storage_info = {
        'name': row['Name of Self Storage'],
        'website': row['Website'] if not pd.isna(row['Website']) else '',
        'email': row['Email / Contact'] if not pd.isna(row['Email / Contact']) else '',
        'phone': row['Telephone Number'] if not pd.isna(row['Telephone Number']) else '',
        'location': row['Location'] if not pd.isna(row['Location']) else '',
        'population': row['Town Population'] if not pd.isna(row['Town Population']) else ''
    }
    
    region_data[region][city].append(storage_info)

# Create region directories and files
for region, cities in region_data.items():
    # Clean region name for URL
    region_clean = re.sub(r'[^\w\s-]', '', region).strip()
    region_clean = re.sub(r'\s+', '-', region_clean)
    
    region_dir = f'website/{region_clean}'
    
    if not os.path.exists(region_dir):
        os.makedirs(region_dir)
    
    # Create region index page
    region_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage in {region} | Find Local Storage Facilities</title>
    <meta name="description" content="Find the best self storage facilities in {region}. Compare prices, locations, and services for all your storage needs.">
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../regions.html">Regions</a></li>
                    <li><a href="../faq.html">FAQ</a></li>
                    <li><a href="../about.html">About</a></li>
                    <li><a href="../contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Self Storage in {region}</h1>
        <p>Find and compare {len(cities)} cities with self storage facilities in {region}.</p>
        
        <div class="search-form">
            <input type="text" id="citySearch" placeholder="Search for a city...">
            <button onclick="searchCity()">Search</button>
        </div>
        
        <h2 id="search-results-heading" style="display: none; margin-top: 30px;">Search Results</h2>
        
        <div class="regions-list">
"""
    
    # Create city cards
    for city, storage_facilities in cities.items():
        city_clean = re.sub(r'[^\w\s-]', '', city).strip()
        city_clean = re.sub(r'\s+', '-', city_clean)
        
        city_dir = f'{region_dir}/{city_clean}'
        if not os.path.exists(city_dir):
            os.makedirs(city_dir)
        
        region_index += f"""
            <div class="region-card">
                <h3>{city}</h3>
                <p>{len(storage_facilities)} storage facilities</p>
                <a href="{city_clean}/index.html" class="btn">View Details</a>
            </div>
"""
        
        # Create city page
        city_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex">
    <title>Self Storage in {city}, {region} | Storage Facilities Near Me</title>
    <meta name="description" content="Find the best self storage facilities in {city}, {region}. Compare prices and services from {len(storage_facilities)} local storage providers.">
    <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="../../index.html">Home</a></li>
                    <li><a href="../../regions.html">Regions</a></li>
                    <li><a href="../../faq.html">FAQ</a></li>
                    <li><a href="../../about.html">About</a></li>
                    <li><a href="../../contact.html">Contact</a></li>
                    <li><a href="../index.html">{region}</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Self Storage in {city}, {region}</h1>
        <p>Compare {len(storage_facilities)} self storage facilities in {city}.</p>
        
        <div class="storage-list">
"""
        
        # Add storage facilities to city page
        for facility in storage_facilities:
            city_page += generate_facility_card(facility)
        
        city_page += """
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="../../privacy.html">Privacy</a></li>
                        <li><a href="../../terms.html">Terms and Conditions</a></li>
                        <li><a href="../../membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="../../index.html">Home</a></li>
                        <li><a href="../../regions.html">Regions</a></li>
                        <li><a href="../../faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="../../about.html">About Us</a></li>
                        <li><a href="../../contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script>
        // Add any JavaScript here
    </script>
</body>
</html>
"""
        
        # Write city page to file
        with open(f'{city_dir}/index.html', 'w', encoding='utf-8') as f:
            f.write(city_page)
    
    # Complete region index
    region_index += """
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="../privacy.html">Privacy</a></li>
                        <li><a href="../terms.html">Terms and Conditions</a></li>
                        <li><a href="../membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="../regions.html">Regions</a></li>
                        <li><a href="../faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="../about.html">About Us</a></li>
                        <li><a href="../contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script src="../assets/js/search.js"></script>
    <script>
        function searchCity() {
            const input = document.getElementById('citySearch').value.toLowerCase();
            const cards = document.querySelectorAll('.region-card');
            
            // Show the search results heading
            document.getElementById('search-results-heading').style.display = 'block';
            
            let anyMatch = false;
            cards.forEach(card => {
                const cityName = card.querySelector('h3').textContent.toLowerCase();
                if (cityName.includes(input)) {
                    card.style.display = 'block';
                    anyMatch = true;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // If no matches, show a message
            if (!anyMatch) {
                alert('No cities found matching your search. Try a different term.');
            }
        }
    </script>
</body>
</html>
"""
    
    # Write region index to file
    with open(f'{region_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(region_index)

# Create regions list page
regions_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage Regions | Find Storage Facilities Near You</title>
    <meta name="description" content="Browse self storage facilities by region across the UK. Find the perfect storage solution in your area.">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .search-container {
            margin-bottom: 30px;
        }
        #citySearchContainer {
            display: none;
        }
        #cityList {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Self Storage Regions</h1>
        <p>Browse self storage facilities by region to find the perfect storage solution near you.</p>
        
        <div id="regionSearchContainer" class="search-container">
            <div class="search-form">
                <input type="text" id="regionSearch" placeholder="Search for a location...">
                <select id="radius">
                    <option value="5">5 miles</option>
                    <option value="10" selected>10 miles</option>
                    <option value="15">15 miles</option>
                    <option value="20">20 miles</option>
                </select>
                <button onclick="searchRegion()">Search</button>
            </div>
            
            <h2 id="search-results-heading" style="display: none; margin-top: 30px;">Search Results</h2>
            
            <div class="regions-list">
"""

# Add region cards
for region, cities in sorted(region_data.items()):
    region_clean = re.sub(r'[^\w\s-]', '', region).strip()
    region_clean = re.sub(r'\s+', '-', region_clean)
    
    total_facilities = sum(len(facilities) for facilities in cities.values())
    
    regions_page += f"""
            <div class="region-card">
                <h3>{region}</h3>
                <p>{len(cities)} cities, {total_facilities} facilities</p>
                <a href="{region_clean}/index.html" class="btn">View Region</a>
            </div>
"""

regions_page += """
            </div>
        </div>
        
        <div id="citySearchContainer" class="search-container" style="display:none;">
            <div id="cityList">
                <!-- City cards will be generated here -->
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script src="assets/js/search.js"></script>
    <script>
        // All cities with their regions and URLs
        const allCities = [
"""

# Create a list of all cities with their regions and URLs
for region, cities in region_data.items():
    region_dir_name = region.replace(' ', '-').replace(',', '')
    for city in cities:
        city_dir_name = city.replace(' ', '-').replace(',', '')
        city_url = f"{region_dir_name}/{city_dir_name}/index.html"
        regions_page += f'            {{name: "{city}", region: "{region}", url: "{city_url}"}},\n'

regions_page += """
        ];
        
        // Function to search regions
        function searchRegion() {
            const input = document.getElementById('regionSearch').value.toLowerCase();
            const radius = document.getElementById('radius').value;
            const cards = document.querySelectorAll('.region-card');
            
            console.log('Searching with radius:', radius);
            
            // Show the search results heading
            document.getElementById('search-results-heading').style.display = 'block';
            
            // First check if the input matches any cities
            const matchingCities = allCities.filter(city => 
                city.name.toLowerCase().includes(input)
            );
            
            // If there's an exact match for a city, redirect to that city page
            const exactMatch = matchingCities.find(city => city.name.toLowerCase() === input);
            if (exactMatch) {
                window.location.href = exactMatch.url;
                return;
            }
            
            // If there are city matches but no exact match, display city results
            if (matchingCities.length > 0) {
                document.getElementById('regionSearchContainer').style.display = 'none';
                document.getElementById('citySearchContainer').style.display = 'block';
                
                const cityListContainer = document.getElementById('cityList');
                cityListContainer.innerHTML = '';
                
                matchingCities.forEach(city => {
                    const cityCard = document.createElement('div');
                    cityCard.className = 'region-card';
                    cityCard.innerHTML = `
                        <h3>${city.name}</h3>
                        <p>${city.region}</p>
                        <a href="${city.url}" class="btn">View Storage</a>
                    `;
                    cityListContainer.appendChild(cityCard);
                });
                return;
            }
            
            // Otherwise, search for regions
            let anyMatch = false;
            cards.forEach(card => {
                const regionName = card.querySelector('h3').textContent.toLowerCase();
                if (regionName.includes(input)) {
                    card.style.display = 'block';
                    anyMatch = true;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // If no matches, show a message
            if (!anyMatch) {
                alert('No regions found matching your search. Try a different term.');
            }
        }
        
        // Check if there's a search parameter
        document.addEventListener('DOMContentLoaded', function() {
            const searchParams = new URLSearchParams(window.location.search);
            if (searchParams.has('search')) {
                const searchTerm = searchParams.get('search');
                const radius = searchParams.has('radius') ? searchParams.get('radius') : '10';
                
                // Set radius dropdown if it exists
                if (document.getElementById('radius')) {
                    document.getElementById('radius').value = radius;
                }
                
                // Set the search term in the region search input
                document.getElementById('regionSearch').value = searchTerm;
                // Execute the search
                searchRegion();
            }
        });
    </script>
</body>
</html>
"""

# Write regions page to file
with open('website/regions.html', 'w', encoding='utf-8') as f:
    f.write(regions_page)

# Create homepage
homepage = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self Storage Near Me | Find Local Storage Facilities</title>
    <meta name="description" content="Find the best self storage facilities near you. Compare prices, locations, and services for all your storage needs.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <h1>Find Self Storage Near Me</h1>
            <p>Compare the best self storage facilities in your area. Find secure, affordable storage solutions for your belongings.</p>
            <div class="search-form">
                <input type="text" id="locationSearch" placeholder="Search for a location...">
                <select id="radius">
                    <option value="5">5 miles</option>
                    <option value="10" selected>10 miles</option>
                    <option value="15">15 miles</option>
                    <option value="20">20 miles</option>
                </select>
                <button onclick="searchLocation()">Search</button>
            </div>
            <a href="regions.html" class="btn">Browse by Region</a>
        </div>
    </section>
    
    <div class="container">
        <h2>Popular Storage Regions</h2>
        <div class="regions-list">
"""

# Add top regions to homepage
top_regions = sorted(region_data.items(), key=lambda x: sum(len(facilities) for facilities in x[1].values()), reverse=True)[:12]

for region, cities in top_regions:
    region_clean = re.sub(r'[^\w\s-]', '', region).strip()
    region_clean = re.sub(r'\s+', '-', region_clean)
    
    total_facilities = sum(len(facilities) for facilities in cities.values())
    
    homepage += f"""
            <div class="region-card">
                <h3>{region}</h3>
                <p>{len(cities)} cities, {total_facilities} facilities</p>
                <a href="{region_clean}/index.html" class="btn">View Region</a>
            </div>
"""

homepage += """
        </div>
        
        <h2>Why Choose Self Storage?</h2>
        <p>Self storage facilities provide a convenient solution for storing personal belongings, business inventory, or seasonal items. Whether you're moving, downsizing, or just need extra space, self storage offers a secure and accessible option.</p>
        
        <div class="regions-list">
            <div class="region-card">
                <h3>Flexible Storage Options</h3>
                <p>Various unit sizes to fit your needs, from small lockers to large rooms.</p>
            </div>
            <div class="region-card">
                <h3>Secure Facilities</h3>
                <p>Most storage facilities offer security features like CCTV, gated access, and on-site staff.</p>
            </div>
            <div class="region-card">
                <h3>Convenient Access</h3>
                <p>Many locations offer 24/7 access to your belongings.</p>
            </div>
            <div class="region-card">
                <h3>Climate Control</h3>
                <p>Protect sensitive items with temperature and humidity-controlled units.</p>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script src="assets/js/search.js"></script>
    <script>
        function searchLocation() {
            const input = document.getElementById('locationSearch').value.toLowerCase();
            const radius = document.getElementById('radius').value;
            
            if (input.trim() === '') {
                alert('Please enter a location to search');
                return;
            }
            
            // Redirect to regions page with search parameter and radius
            window.location.href = 'regions.html?search=' + encodeURIComponent(input) + '&radius=' + radius;
        }
    </script>
</body>
</html>
"""

# Write homepage to file
with open('website/index.html', 'w', encoding='utf-8') as f:
    f.write(homepage)

# Create JavaScript file for advanced search that will work with direct city searches
search_js = """
// This function will search for regions and redirect if found
function searchLocations() {
    const searchTerm = (new URLSearchParams(window.location.search)).get('search');
    if (!searchTerm) return;
    
    const decodedSearchTerm = decodeURIComponent(searchTerm).toLowerCase();
    
    // Try to find a direct match for a region first
    const regionCards = document.querySelectorAll('.region-card');
    let regionFound = false;
    let cityMatches = [];
    
    regionCards.forEach(card => {
        const regionName = card.querySelector('h3').textContent.toLowerCase();
        if (regionName === decodedSearchTerm) {
            const regionUrl = card.querySelector('a.btn').getAttribute('href');
            window.location.href = regionUrl;
            regionFound = true;
        }
        
        // Also check if it contains the term (for partial matches)
        if (regionName.includes(decodedSearchTerm)) {
            card.style.display = 'block';
            regionFound = true;
        } else {
            card.style.display = 'none';
        }
    });
    
    // If we found matches, focus on the search results
    if (regionFound) {
        document.getElementById('search-results-heading').style.display = 'block';
        document.getElementById('search-results-heading').scrollIntoView({ behavior: 'smooth' });
        if (document.getElementById('regionSearch')) {
            document.getElementById('regionSearch').value = decodedSearchTerm;
        }
    }
}

// Function to search for cities within a region
function searchCitiesInRegion() {
    const searchTerm = (new URLSearchParams(window.location.search)).get('search');
    if (!searchTerm) return;
    
    const decodedSearchTerm = decodeURIComponent(searchTerm).toLowerCase();
    const cityCards = document.querySelectorAll('.region-card');
    
    let directMatch = null;
    let anyMatch = false;
    
    cityCards.forEach(card => {
        const cityName = card.querySelector('h3').textContent.toLowerCase();
        
        // Check for exact match first
        if (cityName === decodedSearchTerm) {
            directMatch = card.querySelector('a.btn').getAttribute('href');
        }
        
        // Otherwise show partial matches
        if (cityName.includes(decodedSearchTerm)) {
            card.style.display = 'block';
            anyMatch = true;
        } else {
            card.style.display = 'none';
        }
    });
    
    // If exact match found, redirect
    if (directMatch) {
        window.location.href = directMatch;
        return;
    }
    
    // If partial matches, update the search input and show results
    if (anyMatch) {
        document.getElementById('search-results-heading').style.display = 'block';
        document.getElementById('search-results-heading').scrollIntoView({ behavior: 'smooth' });
        document.getElementById('citySearch').value = decodedSearchTerm;
    }
}

// Initialize the appropriate search function based on the page
document.addEventListener('DOMContentLoaded', function() {
    // If on regions page
    if (document.getElementById('regionSearch')) {
        searchLocations();
    }
    
    // If on a region page with city search
    if (document.getElementById('citySearch') && !document.getElementById('regionSearch')) {
        searchCitiesInRegion();
    }
});
"""

# Create JS directory if it doesn't exist
if not os.path.exists('website/assets/js'):
    os.makedirs('website/assets/js')

# Write search.js to file
with open('website/assets/js/search.js', 'w', encoding='utf-8') as f:
    f.write(search_js)

# Create FAQ page
faq_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frequently Asked Questions About Self Storage | Storage Finder</title>
    <meta name="description" content="Find answers to common questions about self storage including costs, security, access, and more.">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .faq-item {
            background-color: white;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .faq-item h3 {
            color: #0d6efd;
            margin-bottom: 10px;
        }
        
        .faq-item p {
            margin-bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Frequently Asked Questions About Self Storage</h1>
        <p>Find answers to common questions about self storage facilities and services.</p>
        
        <div class="faq-container">
            <div class="faq-item">
                <h3>What is self-storage?</h3>
                <p>A service to rent secured storage space for personal or business items, available in various sizes.</p>
            </div>
            
            <div class="faq-item">
                <h3>How much does it cost to rent a storage unit?</h3>
                <p>Costs vary depending on size, location, and whether it's climate-controlled. In the UK, prices typically range from £10 to £30 per week for a small unit (around 25-50 square feet), averaging about £20 per week or £80-£100 per month for a standard non-climate-controlled unit. Larger units (e.g., 100 square feet) can cost £150-£300 per month, with higher rates in cities like London and lower rates in rural areas.</p>
            </div>
            
            <div class="faq-item">
                <h3>What is the difference between climate-controlled and non-climate-controlled units?</h3>
                <p>Climate-controlled maintains temperature/humidity for sensitive items; non-climate-controlled for sturdy items.</p>
            </div>
            
            <div class="faq-item">
                <h3>How do I know which size unit I need?</h3>
                <p>The right size depends on the volume of items you're storing. For example, a 25 sq ft unit suits small items like a few boxes or a bicycle, while a 50 sq ft unit can hold the contents of a small flat (e.g., a bed, sofa, and some boxes). A 100 sq ft unit is ideal for a one- or two-bedroom home, including furniture and appliances. Visiting the facility can help you estimate the best fit for your needs.</p>
            </div>
            
            <div class="faq-item">
                <h3>What security measures are in place at the facility?</h3>
                <p>Fences, gated entry, cameras, individual locks; some have on-site managers. Check specifics.</p>
            </div>
            
            <div class="faq-item">
                <h3>Can I access my unit at any time?</h3>
                <p>Many offer 24/7 access; some have restricted hours, confirm with facility.</p>
            </div>
            
            <div class="faq-item">
                <h3>What happens if I lose my key or forget my combination?</h3>
                <p>Contact management; they'll assist, often for a fee, by cutting the lock and providing a new one.</p>
            </div>
            
            <div class="faq-item">
                <h3>How do I reserve a storage unit?</h3>
                <p>Online, phone, or in person; provide contact info, may need deposit.</p>
            </div>
            
            <div class="faq-item">
                <h3>What items can I store in a self-storage unit?</h3>
                <p>Furniture, clothing, documents, seasonal items; restrictions on hazardous, perishable, illegal items.</p>
            </div>
            
            <div class="faq-item">
                <h3>Are there any restrictions on what I can store?</h3>
                <p>Yes, no hazardous, flammable, perishable, or illegal items; check facility policies.</p>
            </div>
            
            <div class="faq-item">
                <h3>How long can I rent a storage unit for?</h3>
                <p>Typically month-to-month, flexible for short or long-term needs.</p>
            </div>
            
            <div class="faq-item">
                <h3>What is the notice period for ending my rental?</h3>
                <p>Usually at least one month's notice required to avoid additional charges.</p>
            </div>
            
            <div class="faq-item">
                <h3>What happens if I can't pay my storage bill?</h3>
                <p>May charge late fees, send to collections, or auction contents if unpaid; communicate with facility.</p>
            </div>
            
            <div class="faq-item">
                <h3>Is there insurance available for my stored items?</h3>
                <p>Yes, facilities offer optional insurance; check if homeowner's insurance covers stored items.</p>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# Write FAQ page to file
with open('website/faq.html', 'w', encoding='utf-8') as f:
    f.write(faq_page)

# Create About page
about_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Storage Finder | UK Self Storage Directory</title>
    <meta name="description" content="Learn about Storage Finder, the UK's comprehensive directory of self storage facilities helping you find the perfect storage solution.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>About Storage Finder</h1>
        
        <div style="background-color: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">
            <h2>Our Mission</h2>
            <p>Storage Finder is the UK's most comprehensive directory of self storage facilities. Our mission is to help people find the perfect storage solution for their needs, whether they're moving home, decluttering, storing business inventory, or keeping seasonal items safe.</p>
            
            <h2 style="margin-top: 30px;">What We Offer</h2>
            <p>We provide a detailed database of nearly 3,000 self storage facilities across the UK, covering:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>79 regions across the United Kingdom</li>
                <li>Over 1,200 cities and towns</li>
                <li>Comprehensive contact information for each facility</li>
                <li>Easy navigation by region and city</li>
            </ul>
            
            <h2 style="margin-top: 30px;">Why Use Storage Finder?</h2>
            <p>Finding the right storage facility can be challenging, with various factors to consider such as location, price, security, and specific features. Storage Finder simplifies this process by:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Organizing facilities by geographic location</li>
                <li>Providing direct contact information</li>
                <li>Offering educational resources about self storage through our FAQ section</li>
                <li>Making it easy to compare multiple facilities in your area</li>
            </ul>
            
            <h2 style="margin-top: 30px;">Our Data</h2>
            <p>We maintain an up-to-date database of self storage facilities across the UK. Our information is regularly reviewed to ensure accuracy and completeness. If you're a storage facility owner and would like to update your information or add your facility to our directory, please <a href="contact.html" style="color: #0d6efd;">contact us</a>.</p>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# Write About page to file
with open('website/about.html', 'w', encoding='utf-8') as f:
    f.write(about_page)

# Create Contact Us page
contact_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Storage Finder | UK Self Storage Directory</title>
    <meta name="description" content="Get in touch with Storage Finder for questions, feedback, or to update your storage facility information in our directory.">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .contact-form {
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        
        .form-group textarea {
            height: 150px;
        }
        
        .submit-btn {
            background-color: #0d6efd;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .contact-info {
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .two-columns {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }
        
        @media (max-width: 768px) {
            .two-columns {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Contact Us</h1>
        <p>Have questions, feedback, or need to update information about your storage facility? We'd love to hear from you!</p>
        
        <div class="two-columns">
            <div class="contact-form">
                <h2>Send a Message</h2>
                <form id="contactForm" onsubmit="return false;">
                    <div class="form-group">
                        <label for="name">Your Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <select id="subject" name="subject" required>
                            <option value="">-- Select a Subject --</option>
                            <option value="general">General Inquiry</option>
                            <option value="update">Update Facility Information</option>
                            <option value="add">Add New Facility</option>
                            <option value="feedback">Website Feedback</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="message">Your Message</label>
                        <textarea id="message" name="message" required></textarea>
                    </div>
                    
                    <button type="submit" class="submit-btn" onclick="showThankYou()">Send Message</button>
                </form>
                
                <div id="thankYou" style="display: none; margin-top: 20px; padding: 15px; background-color: #d4edda; color: #155724; border-radius: 5px;">
                    <p>Thank you for your message! We'll get back to you as soon as possible.</p>
                </div>
            </div>
            
            <div class="contact-info">
                <h2>Contact Information</h2>
                <p><strong>Email:</strong> info@storagefinder.co.uk</p>
                <p><strong>Phone:</strong> 020 1234 5678</p>
                <p><strong>Address:</strong><br>
                Storage Finder UK<br>
                123 Storage Lane<br>
                London, EC1A 1BB<br>
                United Kingdom</p>
                
                <h3 style="margin-top: 30px;">Business Hours</h3>
                <p>Monday - Friday: 9:00 AM - 5:00 PM<br>
                Saturday & Sunday: Closed</p>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script>
        function showThankYou() {
            // Basic form validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            if (name && email && subject && message) {
                // Hide form and show thank you message
                document.getElementById('contactForm').style.display = 'none';
                document.getElementById('thankYou').style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

# Write Contact Us page to file
with open('website/contact.html', 'w', encoding='utf-8') as f:
    f.write(contact_page)

# Create Privacy Policy page
privacy_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy | Storage Finder</title>
    <meta name="description" content="Storage Finder's privacy policy explains how we collect, use, and protect your personal information.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Privacy Policy</h1>
        
        <div style="background-color: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">
            <h2>Introduction</h2>
            <p>Storage Finder ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website or use our services.</p>
            
            <h2 style="margin-top: 30px;">Information We Collect</h2>
            <p>We may collect the following types of information:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li><strong>Personal Information:</strong> Name, email address, phone number, and other details you provide when contacting us or using our services.</li>
                <li><strong>Usage Data:</strong> Information about how you access and use our website, including your IP address, browser type, and pages visited.</li>
                <li><strong>Cookies:</strong> We use cookies and similar tracking technologies to enhance your experience on our website.</li>
            </ul>
            
            <h2 style="margin-top: 30px;">How We Use Your Information</h2>
            <p>We use the information we collect to:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Provide and maintain our services</li>
                <li>Improve and personalize your experience</li>
                <li>Respond to your inquiries and provide customer support</li>
                <li>Send you updates, notifications, and marketing communications (with your consent)</li>
                <li>Monitor the usage of our website for improvement and optimization</li>
                <li>Protect our services and prevent fraud</li>
            </ul>
            
            <h2 style="margin-top: 30px;">Data Sharing and Disclosure</h2>
            <p>We may share your information in the following circumstances:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li><strong>Service Providers:</strong> We may share your information with third-party vendors who provide services on our behalf.</li>
                <li><strong>Legal Requirements:</strong> We may disclose your information if required by law or to protect our rights or the rights of others.</li>
                <li><strong>Business Transfers:</strong> In the event of a merger, acquisition, or sale of assets, your information may be transferred as part of the transaction.</li>
            </ul>
            
            <h2 style="margin-top: 30px;">Your Rights</h2>
            <p>Depending on your location, you may have the following rights regarding your personal information:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Access and receive a copy of your data</li>
                <li>Correct or update your data</li>
                <li>Request deletion of your data</li>
                <li>Object to or restrict processing of your data</li>
                <li>Data portability</li>
                <li>Withdraw consent where processing is based on consent</li>
            </ul>
            
            <h2 style="margin-top: 30px;">Security</h2>
            <p>We implement appropriate technical and organizational measures to protect your personal information. However, no method of transmission over the Internet or electronic storage is 100% secure, so we cannot guarantee absolute security.</p>
            
            <h2 style="margin-top: 30px;">Updates to This Policy</h2>
            <p>We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the "Last Updated" date below.</p>
            
            <h2 style="margin-top: 30px;">Contact Us</h2>
            <p>If you have any questions about this Privacy Policy or our data practices, please contact us at:</p>
            <p>Email: privacy@storagefinder.co.uk<br>
            Phone: 020 1234 5678<br>
            Address: Storage Finder UK, 123 Storage Lane, London, EC1A 1BB, United Kingdom</p>
            
            <p style="margin-top: 30px;"><strong>Last Updated:</strong> April 2024</p>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# Write Privacy Policy page to file
with open('website/privacy.html', 'w', encoding='utf-8') as f:
    f.write(privacy_page)

# Create Terms and Conditions page
terms_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms and Conditions | Storage Finder</title>
    <meta name="description" content="The terms and conditions for using Storage Finder's services and website.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Terms and Conditions</h1>
        
        <div style="background-color: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">
            <h2>1. Introduction</h2>
            <p>Welcome to Storage Finder ("the Service"). By accessing or using our website, you agree to be bound by these Terms and Conditions ("Terms"). If you disagree with any part of these Terms, you may not access the Service.</p>
            
            <h2 style="margin-top: 30px;">2. Use of the Service</h2>
            <p>Storage Finder provides a directory of self-storage facilities in the United Kingdom. The Service is intended to help users find storage solutions for their needs. You agree to use the Service only for lawful purposes and in accordance with these Terms.</p>
            
            <h2 style="margin-top: 30px;">3. Information Accuracy</h2>
            <p>We strive to provide accurate and up-to-date information about storage facilities. However, we cannot guarantee the accuracy, completeness, or reliability of any information displayed on our website. The information provided is for general informational purposes only.</p>
            <p>Storage facility details such as prices, availability, and services may change without notice. We recommend contacting the storage facilities directly to confirm current information before making any decisions.</p>
            
            <h2 style="margin-top: 30px;">4. Third-Party Links and Content</h2>
            <p>Our Service may contain links to third-party websites or services that are not owned or controlled by Storage Finder. We have no control over, and assume no responsibility for, the content, privacy policies, or practices of any third-party websites or services.</p>
            <p>You further acknowledge and agree that Storage Finder shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of or reliance on any such content, goods, or services available on or through any such websites or services.</p>
            
            <h2 style="margin-top: 30px;">5. Intellectual Property</h2>
            <p>The Service and its original content, features, and functionality are and will remain the exclusive property of Storage Finder and its licensors. The Service is protected by copyright, trademark, and other laws of both the United Kingdom and foreign countries.</p>
            <p>Our trademarks and trade dress may not be used in connection with any product or service without the prior written consent of Storage Finder.</p>
            
            <h2 style="margin-top: 30px;">6. User Submissions</h2>
            <p>If you submit any information to us, including through our contact forms, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, modify, adapt, publish, translate, and distribute that content in connection with our services.</p>
            <p>You represent and warrant that you own or have the necessary rights to all content you submit, and that such content does not infringe on any third-party rights.</p>
            
            <h2 style="margin-top: 30px;">7. Limitation of Liability</h2>
            <p>In no event shall Storage Finder, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Your access to or use of or inability to access or use the Service</li>
                <li>Any conduct or content of any third party on the Service</li>
                <li>Any content obtained from the Service</li>
                <li>Unauthorized access, use, or alteration of your transmissions or content</li>
            </ul>
            
            <h2 style="margin-top: 30px;">8. Disclaimer</h2>
            <p>Your use of the Service is at your sole risk. The Service is provided on an "AS IS" and "AS AVAILABLE" basis. The Service is provided without warranties of any kind, whether express or implied, including, but not limited to, implied warranties of merchantability, fitness for a particular purpose, non-infringement, or course of performance.</p>
            
            <h2 style="margin-top: 30px;">9. Governing Law</h2>
            <p>These Terms shall be governed and construed in accordance with the laws of the United Kingdom, without regard to its conflict of law provisions.</p>
            <p>Our failure to enforce any right or provision of these Terms will not be considered a waiver of those rights. If any provision of these Terms is held to be invalid or unenforceable by a court, the remaining provisions of these Terms will remain in effect.</p>
            
            <h2 style="margin-top: 30px;">10. Changes to Terms</h2>
            <p>We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at our sole discretion.</p>
            <p>By continuing to access or use our Service after any revisions become effective, you agree to be bound by the revised terms. If you do not agree to the new terms, you are no longer authorized to use the Service.</p>
            
            <h2 style="margin-top: 30px;">11. Contact Us</h2>
            <p>If you have any questions about these Terms, please contact us at:</p>
            <p>Email: legal@storagefinder.co.uk<br>
            Phone: 020 1234 5678<br>
            Address: Storage Finder UK, 123 Storage Lane, London, EC1A 1BB, United Kingdom</p>
            
            <p style="margin-top: 30px;"><strong>Last Updated:</strong> April 2024</p>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# Write Terms and Conditions page to file
with open('website/terms.html', 'w', encoding='utf-8') as f:
    f.write(terms_page)

# Create Membership Terms page
membership_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Membership Terms | Storage Finder</title>
    <meta name="description" content="Terms and conditions for Storage Finder membership and facility listings.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">Storage Finder</div>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="regions.html">Regions</a></li>
                    <li><a href="faq.html">FAQ</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <h1>Membership Terms</h1>
        
        <div style="background-color: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">
            <h2>1. Introduction</h2>
            <p>These Membership Terms govern the relationship between Storage Finder ("we", "our", or "us") and self-storage facilities ("Members") who choose to list their services on our platform.</p>
            
            <h2 style="margin-top: 30px;">2. Membership Types</h2>
            <p>We offer the following membership options for storage facilities:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li><strong>Basic Listing (Free):</strong> Includes facility name, location, and contact information in our directory.</li>
                <li><strong>Standard Membership:</strong> Includes basic listing features plus enhanced visibility in search results, facility photos, and detailed service information.</li>
                <li><strong>Premium Membership:</strong> Includes all standard features plus featured placement in search results, promotional badges, and performance analytics.</li>
            </ul>
            <p>Pricing for paid membership tiers is available upon request and may vary based on location and facility size.</p>
            
            <h2 style="margin-top: 30px;">3. Member Responsibilities</h2>
            <p>As a Member, you agree to:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Provide accurate and up-to-date information about your facility, services, and pricing</li>
                <li>Respond promptly to inquiries from potential customers</li>
                <li>Maintain high standards of customer service</li>
                <li>Notify us of any significant changes to your facility information</li>
                <li>Comply with all applicable laws and regulations</li>
                <li>Not engage in false advertising or deceptive practices</li>
            </ul>
            
            <h2 style="margin-top: 30px;">4. Content and Submissions</h2>
            <p>By submitting content to our platform (including facility descriptions, photos, and other media), you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, modify, adapt, publish, translate, and distribute that content in connection with our services.</p>
            <p>You represent and warrant that you own or have the necessary rights to all content you submit, and that such content does not infringe on any third-party rights.</p>
            
            <h2 style="margin-top: 30px;">5. Term and Termination</h2>
            <p>Paid memberships are billed on a monthly or annual basis, as selected during registration. You may cancel your membership at any time by contacting our customer support team.</p>
            <p>We reserve the right to terminate or suspend your membership at our discretion if you breach these terms or engage in conduct that we determine to be harmful to our platform, users, or reputation.</p>
            
            <h2 style="margin-top: 30px;">6. Payment Terms</h2>
            <p>For paid memberships:</p>
            <ul style="margin-left: 20px; margin-bottom: 20px;">
                <li>Payments are due in advance of the membership period</li>
                <li>Memberships automatically renew unless cancelled before the renewal date</li>
                <li>We accept payment by credit card, debit card, and bank transfer</li>
                <li>Refunds are provided on a case-by-case basis at our discretion</li>
            </ul>
            
            <h2 style="margin-top: 30px;">7. Changes to Membership Terms</h2>
            <p>We may modify these Membership Terms from time to time. We will notify Members of any significant changes via email or through our platform. Your continued use of our services after such modifications constitutes acceptance of the updated terms.</p>
            
            <h2 style="margin-top: 30px;">8. Limitation of Liability</h2>
            <p>Storage Finder is not responsible for the actions or omissions of users who contact you through our platform. We do not guarantee any minimum number of inquiries, bookings, or revenue as a result of your membership.</p>
            <p>In no event shall our liability to any Member exceed the amount paid by that Member for their current membership period.</p>
            
            <h2 style="margin-top: 30px;">9. Dispute Resolution</h2>
            <p>Any disputes arising from or relating to these Membership Terms shall be resolved through good faith negotiation. If we cannot resolve the dispute through negotiation, it shall be submitted to binding arbitration in accordance with UK law.</p>
            
            <h2 style="margin-top: 30px;">10. Contact Information</h2>
            <p>For questions or concerns about your membership, please contact us at:</p>
            <p>Email: membership@storagefinder.co.uk<br>
            Phone: 020 1234 5678<br>
            Address: Storage Finder UK, 123 Storage Lane, London, EC1A 1BB, United Kingdom</p>
            
            <p style="margin-top: 30px;"><strong>Last Updated:</strong> April 2024</p>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <div class="footer-columns">
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy</a></li>
                        <li><a href="terms.html">Terms and Conditions</a></li>
                        <li><a href="membership.html">Membership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Navigate</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="regions.html">Regions</a></li>
                        <li><a href="faq.html">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Storage Finder. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

# Write Membership Terms page to file
with open('website/membership.html', 'w', encoding='utf-8') as f:
    f.write(membership_page)

print("Website generation complete!")
print(f"Total regions: {len(region_data)}")
total_cities = sum(len(cities) for cities in region_data.values())
print(f"Total cities: {total_cities}")
total_facilities = sum(sum(len(facilities) for facilities in cities.values()) for cities in region_data.values())
print(f"Total facilities: {total_facilities}") 