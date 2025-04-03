import os
import re
from bs4 import BeautifulSoup

def fix_search_functionality():
    """
    Fix the search functionality by using the existing search bar on the homepage
    instead of adding a new one.
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
    
    # Remove the search bar we added
    added_search_container = soup.find('div', class_='search-container')
    if added_search_container:
        added_search_container.decompose()
        print("Removed the newly added search bar")
    
    # Find the existing search form in the hero section
    existing_search_form = soup.find('div', class_='search-form')
    
    if existing_search_form:
        # Update the existing search form
        existing_search_form.clear()  # Remove existing content
        
        # Create the input field using the original ID
        search_input = soup.new_tag('input', attrs={
            'type': 'text',
            'id': 'locationSearch',
            'placeholder': 'Enter your location',
            'style': 'padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px 0 0 4px; width: 70%;'
        })
        
        # Create the search button
        search_button = soup.new_tag('button', attrs={
            'onclick': 'searchLocation()',
            'style': 'padding: 12px 24px; background-color: #28A745; color: white; border: none; border-radius: 0 4px 4px 0; cursor: pointer; font-size: 16px;'
        })
        search_button.string = 'Search'
        
        # Add elements to the form
        existing_search_form.append(search_input)
        existing_search_form.append(search_button)
        
        print("Updated the existing search form")
    else:
        print("Error: Could not find the existing search form")
        return
    
    # Remove multiple searchLocation() functions that might be there
    for script in soup.find_all('script'):
        if script.string and 'function searchLocation()' in script.string:
            script.decompose()
    
    # Remove the search-form event listener script added earlier
    for script in soup.find_all('script'):
        if script.string and 'search-form' in script.string:
            script.decompose()
    
    # Create updated JavaScript function to handle search
    script_tag = soup.new_tag('script')
    script_content = """
    function searchLocation() {
        var searchTerm = document.getElementById('locationSearch').value.trim().toLowerCase();
        
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

if __name__ == "__main__":
    fix_search_functionality() 