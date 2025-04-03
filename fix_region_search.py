import os
import json
import re
from bs4 import BeautifulSoup

def improve_region_search():
    """
    Fix the search functionality to handle composite region names correctly
    by prioritizing exact composite matches over partial matches.
    """
    print("Improving search functionality for composite region names...")
    
    # Load the storage site data
    try:
        with open('storage_site_data.json', 'r', encoding='utf-8') as f:
            site_data = json.load(f)
    except Exception as e:
        print(f"Error loading storage site data: {e}")
        return
    
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
    
    # Remove old search location function
    for script in soup.find_all('script'):
        if script.string and 'function searchLocation()' in script.string:
            script.decompose()
    
    # Create a new script tag with improved search functionality
    script_tag = soup.new_tag('script')
    script_content = """
    // All regions and cities data
    var storageSiteData = {
        regions: [
    """
    
    # Add all regions to the JavaScript object
    for region in site_data['regions']:
        script_content += f"""        {{
            name: "{region['name']}",
            path: "{region['path']}",
            display: "{region['name'].replace('-', ' ')}"
        }},
    """
    
    script_content += """    ],
        cities: [
    """
    
    # Add all cities to the JavaScript object
    for city in site_data['cities']:
        script_content += f"""        {{
            name: "{city['name']}",
            path: "{city['path']}",
            region: "{city['region']}",
            display: "{city['name'].replace('-', ' ')}"
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
        
        // First try to find an exact match for composite region names
        var compositeRegionMatch = null;
        
        // These are the composite region names we want to prioritize
        var compositeRegions = [
            // Yorkshire regions
            "west-yorkshire", "east-yorkshire", "south-yorkshire", "north-yorkshire",
            
            // Midlands regions
            "west-midlands", "east-midlands", 
            
            // Somerset regions
            "north-somerset", "south-somerset",
            
            // Scottish regions
            "south-lanarkshire", "north-lanarkshire", 
            "east-dunbartonshire", "west-dunbartonshire",
            "east-lothian", "west-lothian", 
            "north-ayrshire", "east-ayrshire", "south-ayrshire",
            "east-renfrewshire",
            
            // Sussex regions
            "east-sussex", "west-sussex",
            
            // Islands and composite names
            "shetland-islands", "western-isles", "orkney-islands",
            "isle-of-wight", "isle-of-man", "isle-of-anglesey",
            
            // Other composite regions
            "tyne-and-wear", "greater-london", "greater-manchester"
        ];
        
        // Special cases with alternative forms
        var specialCases = {
            "shetland": "shetland-islands",
            "orkney": "orkney-islands",
            "western isles": "western-isles",
            "isle of wight": "isle-of-wight",
            "isle of man": "isle-of-man",
            "isle of anglesey": "isle-of-anglesey",
            "anglesey": "isle-of-anglesey",
            "manchester": "greater-manchester",
            "london": "greater-london"
        };
        
        // Check special cases first
        if (specialCases[searchTerm]) {
            formattedSearch = specialCases[searchTerm];
        }
        
        // Then check composite regions
        for (var c = 0; c < compositeRegions.length; c++) {
            var compositeRegion = compositeRegions[c];
            var compositeDisplay = compositeRegion.replace(/-/g, ' '); // Replace all hyphens, not just the first one
            
            // Check if search term is the composite region
            if (searchTerm === compositeDisplay || formattedSearch === compositeRegion) {
                // Find the matching region in our data
                for (var r = 0; r < storageSiteData.regions.length; r++) {
                    if (storageSiteData.regions[r].name === compositeRegion) {
                        compositeRegionMatch = storageSiteData.regions[r];
                        break;
                    }
                }
                if (compositeRegionMatch) break;
            }
        }
        
        // If we found a composite region match, go to it immediately
        if (compositeRegionMatch) {
            console.log("Going to composite region match: " + compositeRegionMatch.path);
            window.location.href = compositeRegionMatch.path;
            return;
        }
        
        // Next try to find an exact city match
        var exactCityMatch = null;
        var partialCityMatches = [];
        
        for (var i = 0; i < storageSiteData.cities.length; i++) {
            var city = storageSiteData.cities[i];
            
            // Check for exact match by name or display name
            if (city.name === formattedSearch || city.display === searchTerm) {
                console.log("Found exact city match: " + city.name);
                exactCityMatch = city;
                break;
            }
            
            // Check for partial match (city name contains search term or vice versa)
            if (city.name.includes(formattedSearch) || 
                city.display.includes(searchTerm) ||
                searchTerm.includes(city.display)) {
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
            if (region.name === formattedSearch || region.display === searchTerm) {
                console.log("Found exact region match: " + region.name);
                exactRegionMatch = region;
                break;
            }
            
            // Check for partial match - but be more careful with region names
            // Only count it as a partial match if the region name starts with the search term
            // This prevents "land" matching "Scotland" or "land" matching "England"
            if (region.name.startsWith(formattedSearch) || 
                region.display.startsWith(searchTerm)) {
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
    
    print("Search functionality improvement complete!")

if __name__ == "__main__":
    improve_region_search() 