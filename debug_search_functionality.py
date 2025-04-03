import os
import re
import glob
from bs4 import BeautifulSoup

def debug_search_functionality():
    """
    Debug and fix the search functionality by correcting the URL paths.
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
    for root, dirs, files in os.walk('website'):
        if 'index.html' in files:
            path = os.path.relpath(os.path.join(root, 'index.html'), 'website')
            if 'selfstorage' in path:
                # This is likely a city or region page
                if path.count('/') == 1:
                    # Direct subdirectory of website - likely a region
                    region_paths.append(path)
                elif path.count('/') == 2:
                    # Two levels deep - likely a city within a region
                    city_paths.append(path)
    
    print(f"Found {len(region_paths)} region pages and {len(city_paths)} city pages")
    
    # Now let's check the structure of a few paths to understand the pattern
    if region_paths:
        print(f"Sample region paths: {region_paths[:3]}")
    if city_paths:
        print(f"Sample city paths: {city_paths[:3]}")
    
    # Read the homepage
    try:
        with open(homepage_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading homepage: {e}")
        return
    
    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Create updated JavaScript function to handle search with proper URL handling
    for script in soup.find_all('script'):
        if script.string and 'function searchLocation()' in script.string:
            script.decompose()
    
    # Create our improved search function
    script_tag = soup.new_tag('script')
    script_content = """
    function searchLocation() {
        var searchTerm = document.getElementById('locationSearch').value.trim().toLowerCase();
        
        if (!searchTerm) {
            alert('Please enter a city or region name');
            return;
        }
        
        // Format the search term for URL matching
        var formattedSearch = searchTerm.replace(/\\s+/g, '-');
        
        // Search logic for city pages
        var cityFound = false;
        var cityPages = [
    """
    
    # Add city paths as an array in JavaScript
    for path in city_paths[:100]:  # Limit to first 100 for performance
        # Extract the city name from the path
        city_name = path.split('/')[-2]
        if city_name.startswith('selfstorage'):
            city_name = city_name[11:]  # Remove 'selfstorage' prefix
        script_content += f'        "{path}",\n'
    
    script_content += """
        ];
        
        // Search through city pages
        for (var i = 0; i < cityPages.length; i++) {
            var cityPath = cityPages[i];
            var cityName = cityPath.split('/')[1].replace('selfstorage', '');
            
            if (cityName === formattedSearch) {
                // Exact match found
                window.location.href = cityPath;
                cityFound = true;
                break;
            }
        }
        
        // If no city match, try looking at region pages
        if (!cityFound) {
            var regionPages = [
    """
    
    # Add region paths as an array in JavaScript
    for path in region_paths:
        # Extract the region name from the path
        region_name = path.split('/')[0]
        if region_name.startswith('selfstorage'):
            region_name = region_name[11:]  # Remove 'selfstorage' prefix
        script_content += f'        "{path}",\n'
    
    script_content += """
            ];
            
            // Search through region pages
            var regionFound = false;
            for (var j = 0; j < regionPages.length; j++) {
                var regionPath = regionPages[j];
                var regionName = regionPath.split('/')[0].replace('selfstorage', '');
                
                if (regionName === formattedSearch) {
                    // Exact match found
                    window.location.href = regionPath;
                    regionFound = true;
                    break;
                }
            }
            
            // If still no match, go to regions page with search parameter
            if (!regionFound) {
                window.location.href = 'selfstorageregions/index.html?search=' + formattedSearch;
            }
        }
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
    
    # Also check if search.js exists for the regions page
    if not os.path.exists('website/js/search.js'):
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
                        const formattedSearch = searchTerm.toLowerCase().replace(/-/g, ' ');
                        
                        // Find all region links
                        const regionLinks = document.querySelectorAll('a');
                        
                        // Flag to check if we found a match
                        let foundMatch = false;
                        
                        // Check each link
                        regionLinks.forEach(function(link) {
                            const linkText = link.textContent.toLowerCase();
                            const href = link.getAttribute('href');
                            
                            if (linkText.includes(formattedSearch) || 
                                (href && href.toLowerCase().includes(formattedSearch))) {
                                // Match found, highlight and scroll to it
                                link.style.backgroundColor = '#e8f5e9';
                                link.style.padding = '5px';
                                link.style.borderRadius = '4px';
                                link.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                foundMatch = true;
                            }
                        });
                        
                        // If no match, show message
                        if (!foundMatch) {
                            const message = document.createElement('div');
                            message.style.padding = '15px';
                            message.style.margin = '20px 0';
                            message.style.backgroundColor = '#f8d7da';
                            message.style.color = '#721c24';
                            message.style.borderRadius = '4px';
                            message.textContent = 'No regions or cities found matching "' + 
                                searchTerm.replace(/-/g, ' ') + '". Please try a different search.';
                            
                            const container = document.querySelector('.container');
                            if (container) {
                                container.insertBefore(message, container.firstChild);
                            } else {
                                document.body.insertBefore(message, document.body.firstChild);
                            }
                        }
                    }
                });
                """)
            print("Created improved search.js file")
        except Exception as e:
            print(f"Error creating search.js file: {e}")

if __name__ == "__main__":
    debug_search_functionality() 