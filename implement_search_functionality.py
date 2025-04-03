import os
import re
from bs4 import BeautifulSoup

def implement_search_functionality():
    """
    Implement a functional search bar on the homepage that redirects to the appropriate
    region or city page when a user searches for a region or city.
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
    
    # Find existing search form or create a new one
    search_form = soup.find('form', {'id': 'search-form'})
    
    if not search_form:
        # Create a search form if it doesn't exist
        # Look for a container where the search form should be added
        main_container = soup.find('div', class_='container')
        
        if not main_container:
            print("Error: Could not find a suitable container for the search form")
            return
        
        # Create the search form HTML
        search_div = soup.new_tag('div', attrs={'class': 'search-container', 'style': 'margin: 40px auto; max-width: 800px; text-align: center;'})
        
        # Add a heading
        search_heading = soup.new_tag('h2')
        search_heading.string = 'Find Storage in Your Area'
        search_div.append(search_heading)
        
        # Add a paragraph
        search_text = soup.new_tag('p')
        search_text.string = 'Enter your city or region to find self storage facilities near you'
        search_div.append(search_text)
        
        # Create the form
        search_form = soup.new_tag('form', attrs={
            'id': 'search-form',
            'style': 'display: flex; max-width: 600px; margin: 20px auto;'
        })
        
        # Create the input field
        search_input = soup.new_tag('input', attrs={
            'type': 'text',
            'id': 'search-input',
            'placeholder': 'Enter city or region name...',
            'style': 'flex: 1; padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px 0 0 4px;'
        })
        
        # Create the search button
        search_button = soup.new_tag('button', attrs={
            'type': 'submit',
            'style': 'padding: 12px 24px; background-color: #28A745; color: white; border: none; border-radius: 0 4px 4px 0; cursor: pointer; font-size: 16px;'
        })
        search_button.string = 'Search'
        
        # Assemble the form
        search_form.append(search_input)
        search_form.append(search_button)
        
        # Add the form to the search container
        search_div.append(search_form)
        
        # Insert the search container after the first main container
        main_container.insert(1, search_div)
    
    # Create JavaScript function to handle search
    script_tag = soup.new_tag('script')
    script_content = """
    document.getElementById('search-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        var searchTerm = document.getElementById('search-input').value.trim().toLowerCase();
        
        if (!searchTerm) {
            alert('Please enter a city or region name');
            return;
        }
        
        // Format the search term for URL matching
        searchTerm = searchTerm.replace(/\\s+/g, '-');
        
        // First try to find an exact city match
        var cityUrl = 'selfstorageregions/' + searchTerm + '/index.html';
        var xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // City page found, redirect
                    window.location.href = cityUrl;
                } else {
                    // Try to find the region
                    var regionUrl = 'selfstorageregions/index.html';
                    window.location.href = regionUrl + '?search=' + searchTerm;
                }
            }
        };
        
        xhr.open('HEAD', cityUrl, true);
        xhr.send();
    });
    """
    script_tag.string = script_content
    
    # Add the script tag to the page
    soup.body.append(script_tag)
    
    # Also create a search.js file to be used on the regions page
    regions_script = """
    document.addEventListener('DOMContentLoaded', function() {
        // Check if there's a search parameter in the URL
        const urlParams = new URLSearchParams(window.location.search);
        const searchTerm = urlParams.get('search');
        
        if (searchTerm) {
            // Format the search term for comparison
            const formattedSearch = searchTerm.toLowerCase().replace(/-/g, ' ');
            
            // Find all region links
            const regionLinks = document.querySelectorAll('.region-list a');
            
            // Flag to check if we found a match
            let foundMatch = false;
            
            // Check each region
            regionLinks.forEach(function(link) {
                const regionName = link.textContent.toLowerCase();
                
                if (regionName.includes(formattedSearch)) {
                    // Region found, highlight and scroll to it
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
                message.textContent = 'No regions found matching "' + searchTerm.replace(/-/g, ' ') + '". Please try a different search.';
                
                const container = document.querySelector('.container');
                container.insertBefore(message, container.firstChild);
            }
        }
    });
    """
    
    # Create the JavaScript file for the regions page
    try:
        os.makedirs('website/js', exist_ok=True)
        with open('website/js/search.js', 'w', encoding='utf-8') as f:
            f.write(regions_script)
        print("Created search.js file for regions page")
    except Exception as e:
        print(f"Error creating search.js file: {e}")
    
    # Now we need to modify the regions page to include the search.js script
    regions_page_path = 'website/selfstorageregions/index.html'
    
    if os.path.exists(regions_page_path):
        try:
            with open(regions_page_path, 'r', encoding='utf-8') as f:
                regions_content = f.read()
            
            regions_soup = BeautifulSoup(regions_content, 'html.parser')
            
            # Add the script tag reference
            regions_script_tag = regions_soup.new_tag('script', attrs={'src': '../js/search.js'})
            regions_soup.body.append(regions_script_tag)
            
            with open(regions_page_path, 'w', encoding='utf-8') as f:
                f.write(str(regions_soup))
            
            print(f"Updated regions page with search script")
        except Exception as e:
            print(f"Error updating regions page: {e}")
    else:
        print(f"Regions page not found at {regions_page_path}")
    
    # Save the modified homepage
    try:
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Successfully implemented search functionality on the homepage")
    except Exception as e:
        print(f"Error saving homepage: {e}")

if __name__ == "__main__":
    implement_search_functionality() 