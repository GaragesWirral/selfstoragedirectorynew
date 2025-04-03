
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
            