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