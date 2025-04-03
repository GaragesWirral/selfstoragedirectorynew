import os
import re
import json
from bs4 import BeautifulSoup

def find_all_storage_pages():
    """
    Explicitly analyze the website directory structure and create a comprehensive
    list of all region and city pages for better search functionality.
    """
    print("Starting to analyze website directory structure...")
    
    # Path to the website directory
    website_dir = 'website'
    
    # Ensure the website directory exists
    if not os.path.exists(website_dir):
        print(f"Error: Website directory not found at {website_dir}")
        return
    
    # Lists to store region and city paths
    regions = []
    cities = []
    
    # Direct subdirectories of the website directory are likely regions
    for item in os.listdir(website_dir):
        item_path = os.path.join(website_dir, item)
        
        if os.path.isdir(item_path) and item.startswith('selfstorage'):
            # This is likely a region directory
            region_name = item.replace('selfstorage', '')
            index_file = os.path.join(item_path, 'index.html')
            
            if os.path.exists(index_file):
                # Add the region to our list
                region_path = f"{item}/index.html"
                regions.append({
                    'name': region_name,
                    'path': region_path
                })
                print(f"Found region: {region_name} - {region_path}")
                
                # Look for cities within this region
                for city_item in os.listdir(item_path):
                    city_path = os.path.join(item_path, city_item)
                    
                    if os.path.isdir(city_path) and city_item.startswith('selfstorage'):
                        # This is likely a city directory
                        city_name = city_item.replace('selfstorage', '')
                        city_index = os.path.join(city_path, 'index.html')
                        
                        if os.path.exists(city_index):
                            # Add the city to our list
                            full_city_path = f"{item}/{city_item}/index.html"
                            cities.append({
                                'name': city_name,
                                'path': full_city_path,
                                'region': region_name
                            })
                            print(f"Found city: {city_name} in {region_name} - {full_city_path}")
    
    print(f"Analysis complete. Found {len(regions)} regions and {len(cities)} cities.")
    
    # Path to the homepage
    homepage_path = os.path.join(website_dir, 'index.html')
    
    # Check if homepage exists
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage not found at {homepage_path}")
        return
    
    # Read the homepage
    try:
        with open(homepage_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading homepage: {e}")
        return
    
    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove old search location function
    for script in soup.find_all('script'):
        if script.string and 'function searchLocation()' in script.string:
            script.decompose()
    
    # Create JSON for easier debugging
    site_data = {
        'regions': regions,
        'cities': cities
    }
    
    try:
        with open('storage_site_data.json', 'w', encoding='utf-8') as f:
            json.dump(site_data, f, indent=2)
        print("Saved site data to storage_site_data.json for debugging")
    except Exception as e:
        print(f"Error saving site data: {e}")
    
    # Create a comprehensive JavaScript object with all regions and cities
    script_tag = soup.new_tag('script')
    script_content = """
    // All regions and cities data
    var storageSiteData = {
        regions: [
    """
    
    # Add all regions to the JavaScript object
    for region in regions:
        script_content += f"""        {{
            name: "{region['name']}",
            path: "{region['path']}"
        }},
    """
    
    script_content += """    ],
        cities: [
    """
    
    # Add all cities to the JavaScript object
    for city in cities:
        script_content += f"""        {{
            name: "{city['name']}",
            path: "{city['path']}",
            region: "{city['region']}"
        }},
    """
    
    script_content += """    ]
    };
    
    function searchLocation() {
        var searchTerm = document.getElementById('locationSearch').value.trim().toLowerCase();
        
        if (!searchTerm) {
            alert('Please enter a city or region name');
            return;
        }
        
        console.log("Searching for: " + searchTerm);
        
        // Format the search term for matching
        var formattedSearch = searchTerm.replace(/\\s+/g, '-');
        
        // First try to find an exact city match
        var exactCityMatch = null;
        var partialCityMatches = [];
        
        for (var i = 0; i < storageSiteData.cities.length; i++) {
            var city = storageSiteData.cities[i];
            
            // Check for exact match
            if (city.name === formattedSearch || city.name === searchTerm) {
                console.log("Found exact city match: " + city.name);
                exactCityMatch = city;
                break;
            }
            
            // Check for partial match (city name contains search term or vice versa)
            if (city.name.includes(formattedSearch) || 
                city.name.includes(searchTerm) ||
                searchTerm.includes(city.name)) {
                console.log("Found partial city match: " + city.name);
                partialCityMatches.push(city);
            }
        }
        
        // If we found an exact city match, go to it
        if (exactCityMatch) {
            console.log("Going to exact city match: " + exactCityMatch.path);
            window.location.href = exactCityMatch.path;
            return;
        }
        
        // If we have partial city matches, use the first one (most relevant)
        if (partialCityMatches.length > 0) {
            console.log("Going to partial city match: " + partialCityMatches[0].path);
            window.location.href = partialCityMatches[0].path;
            return;
        }
        
        // No city match, try to find a region match
        var exactRegionMatch = null;
        var partialRegionMatches = [];
        
        for (var j = 0; j < storageSiteData.regions.length; j++) {
            var region = storageSiteData.regions[j];
            
            // Check for exact match
            if (region.name === formattedSearch || region.name === searchTerm) {
                console.log("Found exact region match: " + region.name);
                exactRegionMatch = region;
                break;
            }
            
            // Check for partial match
            if (region.name.includes(formattedSearch) || 
                region.name.includes(searchTerm) ||
                searchTerm.includes(region.name)) {
                console.log("Found partial region match: " + region.name);
                partialRegionMatches.push(region);
            }
        }
        
        // If we found an exact region match, go to it
        if (exactRegionMatch) {
            console.log("Going to exact region match: " + exactRegionMatch.path);
            window.location.href = exactRegionMatch.path;
            return;
        }
        
        // If we have partial region matches, use the first one
        if (partialRegionMatches.length > 0) {
            console.log("Going to partial region match: " + partialRegionMatches[0].path);
            window.location.href = partialRegionMatches[0].path;
            return;
        }
        
        // No matches found, go to regions page with search term
        console.log("No matches found, going to regions page");
        window.location.href = 'selfstorageregions/index.html?search=' + encodeURIComponent(searchTerm);
    }
    """
    
    script_tag.string = script_content
    
    # Add the script tag to the page
    soup.body.append(script_tag)
    
    # Save the modified homepage
    try:
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Successfully updated the search functionality on the homepage")
    except Exception as e:
        print(f"Error saving homepage: {e}")
    
    # Update the search.js file for the regions page
    try:
        os.makedirs(os.path.join(website_dir, 'js'), exist_ok=True)
        with open(os.path.join(website_dir, 'js', 'search.js'), 'w', encoding='utf-8') as f:
            f.write("""
            document.addEventListener('DOMContentLoaded', function() {
                // Check if there's a search parameter in the URL
                const urlParams = new URLSearchParams(window.location.search);
                const searchTerm = urlParams.get('search');
                
                if (searchTerm) {
                    // Format the search term for comparison
                    const formattedSearch = searchTerm.toLowerCase();
                    
                    console.log("Searching regions page for: " + formattedSearch);
                    
                    // Search for matching regions and cities
                    const allLinks = document.querySelectorAll('a');
                    let foundMatch = false;
                    let matchCount = 0;
                    
                    // Check each link for matches in text or href
                    allLinks.forEach(function(link) {
                        const linkText = link.textContent.toLowerCase();
                        const href = link.getAttribute('href') || '';
                        
                        // Check if the link contains our search term or vice versa
                        if (linkText.includes(formattedSearch) || 
                            formattedSearch.includes(linkText) ||
                            href.toLowerCase().includes(formattedSearch.replace(/-/g, '')) ||
                            formattedSearch.replace(/-/g, '').includes(href.toLowerCase())) {
                            
                            console.log("Found match: " + linkText + " - " + href);
                            
                            // Match found, highlight it
                            link.style.backgroundColor = '#e8f5e9';
                            link.style.padding = '5px';
                            link.style.borderRadius = '4px';
                            matchCount++;
                            
                            // Only scroll to the first match
                            if (!foundMatch) {
                                link.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                foundMatch = true;
                            }
                        }
                    });
                    
                    // Show a message about the matches
                    const message = document.createElement('div');
                    message.style.padding = '15px';
                    message.style.margin = '20px 0';
                    
                    if (foundMatch) {
                        message.style.backgroundColor = '#d4edda';
                        message.style.color = '#155724';
                        message.style.borderRadius = '4px';
                        message.textContent = 'Found ' + matchCount + ' matches for "' + 
                            searchTerm + '". Matching links are highlighted below.';
                    } else {
                        message.style.backgroundColor = '#f8d7da';
                        message.style.color = '#721c24';
                        message.style.borderRadius = '4px';
                        message.textContent = 'No regions or cities found matching "' + 
                            searchTerm + '". Please try a different search.';
                    }
                    
                    const container = document.querySelector('.container');
                    if (container) {
                        container.insertBefore(message, container.firstChild);
                    } else {
                        document.body.insertBefore(message, document.body.firstChild);
                    }
                }
            });
            """)
        print("Updated search.js file for regions page")
    except Exception as e:
        print(f"Error updating search.js file: {e}")

if __name__ == "__main__":
    find_all_storage_pages() 