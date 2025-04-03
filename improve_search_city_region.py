import os
import re
import glob
from bs4 import BeautifulSoup

def improve_search_city_region():
    """
    Create a comprehensive search functionality that accurately finds both city and region pages
    by collecting all actual paths and building a correct mapping.
    """
    # Path to the homepage
    homepage_path = 'website/index.html'
    
    # Check if homepage exists
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage not found at {homepage_path}")
        return
    
    # First, let's map all available cities and regions for accurate search matching
    city_paths = []
    region_paths = []
    
    # Walk through the website directory to find all city and region pages
    print("Collecting region and city paths...")
    for root, dirs, files in os.walk('website'):
        if 'index.html' in files:
            path = os.path.relpath(os.path.join(root, 'index.html'), 'website')
            if 'selfstorage' in path:
                parts = path.split('/')
                if len(parts) == 2:  # Region page (e.g., "selfstoragedevon/index.html")
                    region_name = parts[0].replace('selfstorage', '')
                    region_paths.append({
                        'path': path,
                        'name': region_name
                    })
                elif len(parts) == 3:  # City page (e.g., "selfstorageberkshire/selfstoragewindsor/index.html")
                    city_name = parts[1].replace('selfstorage', '')
                    city_paths.append({
                        'path': path,
                        'name': city_name,
                        'region': parts[0].replace('selfstorage', '')
                    })
    
    print(f"Found {len(region_paths)} region pages and {len(city_paths)} city pages")
    
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
    
    # Create a comprehensive JavaScript object with all regions and cities
    # This will enable fast client-side searching
    script_tag = soup.new_tag('script')
    script_content = """
    // All regions and cities data
    var storageSiteData = {
        regions: [
    """
    
    # Add all regions to the JavaScript object
    for region in region_paths:
        script_content += f"""        {{
            name: "{region['name']}",
            path: "{region['path']}"
        }},
    """
    
    script_content += """    ],
        cities: [
    """
    
    # Add all cities to the JavaScript object
    for city in city_paths:
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
        
        // Format the search term for matching
        var formattedSearch = searchTerm.replace(/\\s+/g, '-');
        
        // First try to find an exact city match
        var exactCityMatch = null;
        var partialCityMatches = [];
        
        for (var i = 0; i < storageSiteData.cities.length; i++) {
            var city = storageSiteData.cities[i];
            
            // Check for exact match
            if (city.name === formattedSearch || city.name === searchTerm) {
                exactCityMatch = city;
                break;
            }
            
            // Check for partial match (city name contains search term)
            if (city.name.includes(formattedSearch) || 
                city.name.includes(searchTerm) ||
                searchTerm.includes(city.name)) {
                partialCityMatches.push(city);
            }
        }
        
        // If we found an exact city match, go to it
        if (exactCityMatch) {
            window.location.href = exactCityMatch.path;
            return;
        }
        
        // If we have partial city matches, use the first one (most relevant)
        if (partialCityMatches.length > 0) {
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
                exactRegionMatch = region;
                break;
            }
            
            // Check for partial match
            if (region.name.includes(formattedSearch) || 
                region.name.includes(searchTerm) ||
                searchTerm.includes(region.name)) {
                partialRegionMatches.push(region);
            }
        }
        
        // If we found an exact region match, go to it
        if (exactRegionMatch) {
            window.location.href = exactRegionMatch.path;
            return;
        }
        
        // If we have partial region matches, use the first one
        if (partialRegionMatches.length > 0) {
            window.location.href = partialRegionMatches[0].path;
            return;
        }
        
        // No matches found, go to regions page with search term
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
        os.makedirs('website/js', exist_ok=True)
        with open('website/js/search.js', 'w', encoding='utf-8') as f:
            f.write("""
            document.addEventListener('DOMContentLoaded', function() {
                // Check if there's a search parameter in the URL
                const urlParams = new URLSearchParams(window.location.search);
                const searchTerm = urlParams.get('search');
                
                if (searchTerm) {
                    // Format the search term for comparison
                    const formattedSearch = searchTerm.toLowerCase();
                    
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
    improve_search_city_region() 