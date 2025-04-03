import os
import re
import glob
from bs4 import BeautifulSoup

def fix_search_paths():
    """
    Fix the search functionality by correctly handling the website structure.
    The website has a structure like:
    - website/selfstorageregion-name/ (region pages)
    - website/selfstorageregion-name/selfstoragecity-name/ (city pages)
    """
    # Path to the homepage
    homepage_path = 'website/index.html'
    
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
        
        // First check if it's a direct city search (e.g., "london")
        // Try common regions that might contain this city
        var regions = document.querySelectorAll('.regions-list .region-card a');
        var regionUrls = [];
        
        // Build a list of region URLs to try
        for (var i = 0; i < regions.length; i++) {
            if (regions[i].href) {
                regionUrls.push(regions[i].href);
            }
        }
        
        // If we couldn't find regions from the page, use some hardcoded common regions
        if (regionUrls.length === 0) {
            regionUrls = [
                'selfstoragegreater-london/index.html',
                'selfstoragewest-yorkshire/index.html',
                'selfstoragegreater-manchester/index.html',
                'selfstorageberkshire/index.html',
                'selfstoragedevon/index.html',
                'selfstoragesurrey/index.html',
                'selfstoragehampshire/index.html',
                'selfstoragekent/index.html',
                'selfstorageessex/index.html',
                'selfstoragebristol/index.html'
            ];
        }
        
        // First try direct region match
        var directRegionUrl = 'selfstorage' + formattedSearch + '/index.html';
        
        // Check if the region exists
        var xhr = new XMLHttpRequest();
        xhr.open('HEAD', directRegionUrl, false); // Synchronous for simplicity
        
        try {
            xhr.send();
            if (xhr.status === 200) {
                // Region exists, redirect to it
                window.location.href = directRegionUrl;
                return;
            }
        } catch (e) {
            // Error checking region, continue to other options
            console.log('Error checking region: ' + e);
        }
        
        // If no direct region match, try the regions page with search parameter
        window.location.href = 'selfstorageregions/index.html?search=' + formattedSearch;
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
                    
                    // Check each link for matches in text or href
                    allLinks.forEach(function(link) {
                        const linkText = link.textContent.toLowerCase();
                        const href = link.getAttribute('href') || '';
                        
                        // Check if the link contains our search term
                        if (linkText.includes(formattedSearch) || 
                            href.toLowerCase().includes(formattedSearch.replace(/-/g, ''))) {
                            
                            // Match found, highlight and scroll to it
                            link.style.backgroundColor = '#e8f5e9';
                            link.style.padding = '5px';
                            link.style.borderRadius = '4px';
                            
                            // Only scroll to the first match
                            if (!foundMatch) {
                                link.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                foundMatch = true;
                            }
                        }
                    });
                    
                    // If no match was found, show a message
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
        print("Created improved search.js file for regions page")
    except Exception as e:
        print(f"Error creating search.js file: {e}")
    
    # Make sure the regions page has the script included
    regions_page_path = 'website/selfstorageregions/index.html'
    if os.path.exists(regions_page_path):
        try:
            with open(regions_page_path, 'r', encoding='utf-8') as f:
                regions_content = f.read()
            
            regions_soup = BeautifulSoup(regions_content, 'html.parser')
            
            # Check if the script is already included
            script_exists = False
            for script in regions_soup.find_all('script'):
                src = script.get('src')
                if src and 'search.js' in src:
                    script_exists = True
                    break
            
            if not script_exists:
                # Add the script tag reference
                regions_script_tag = regions_soup.new_tag('script', attrs={'src': '../js/search.js'})
                regions_soup.body.append(regions_script_tag)
                
                with open(regions_page_path, 'w', encoding='utf-8') as f:
                    f.write(str(regions_soup))
                
                print(f"Added search.js script to regions page")
            else:
                print(f"Search script already included in regions page")
        except Exception as e:
            print(f"Error updating regions page: {e}")
    else:
        print(f"Regions page not found at {regions_page_path}")

if __name__ == "__main__":
    fix_search_paths() 