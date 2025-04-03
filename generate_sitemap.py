import os
import re
from pathlib import Path
from datetime import datetime
import xml.dom.minidom as md

def generate_sitemap():
    """Generate an XML sitemap for search engines by crawling through the website directory."""
    website_dir = Path("website")
    base_url = "https://storagefinder.uk"
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create XML document
    doc = md.getDOMImplementation().createDocument(None, "urlset", None)
    root = doc.documentElement
    root.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Track unique URLs to avoid duplicates
    processed_urls = set()
    
    # Priority mapping based on path depth and page type
    def get_priority(path):
        if path == "index.html" or path == "":
            return "1.0"
        elif "regions" in path:
            return "0.9"
        elif any(key in path for key in ["about", "contact", "faq", "calculator"]):
            return "0.8"
        elif any(key in path for key in ["privacy", "terms", "membership"]):
            return "0.5"
        else:
            # Calculate priority based on path depth
            depth = path.count("/")
            if depth == 1:  # Region page
                return "0.8"
            elif depth == 2:  # City page
                return "0.7"
            else:
                return "0.6"
    
    # Change frequency based on page type
    def get_changefreq(path):
        if "index.html" in path and "/" not in path.replace("index.html", ""):
            return "weekly"
        elif any(key in path for key in ["privacy", "terms", "membership"]):
            return "yearly"
        elif any(key in path for key in ["about", "contact", "faq"]):
            return "monthly"
        else:
            return "weekly"
    
    # Process all HTML files
    for root_dir, _, files in os.walk(website_dir):
        for file in files:
            if file.endswith(".html"):
                # Get relative path
                file_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(file_path, website_dir)
                
                # Convert Windows paths to URL paths
                url_path = rel_path.replace("\\", "/")
                
                # Create full URL
                full_url = f"{base_url}/{url_path}"
                
                # Skip if already processed
                if full_url in processed_urls:
                    continue
                
                processed_urls.add(full_url)
                
                # Create URL element
                url_element = doc.createElement("url")
                
                # Add location
                loc = doc.createElement("loc")
                loc_text = doc.createTextNode(full_url)
                loc.appendChild(loc_text)
                url_element.appendChild(loc)
                
                # Add last modified date
                lastmod = doc.createElement("lastmod")
                lastmod_text = doc.createTextNode(today)
                lastmod.appendChild(lastmod_text)
                url_element.appendChild(lastmod)
                
                # Add change frequency
                changefreq = doc.createElement("changefreq")
                freq = get_changefreq(url_path)
                changefreq_text = doc.createTextNode(freq)
                changefreq.appendChild(changefreq_text)
                url_element.appendChild(changefreq)
                
                # Add priority
                priority = doc.createElement("priority")
                pri = get_priority(url_path)
                priority_text = doc.createTextNode(pri)
                priority.appendChild(priority_text)
                url_element.appendChild(priority)
                
                # Add URL to root
                root.appendChild(url_element)
    
    # Write XML to file
    xml_str = doc.toprettyxml(indent="  ")
    
    # Clean up extra whitespace
    xml_str = re.sub(r'\n\s*\n', '\n', xml_str)
    
    with open("website/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
    
    print(f"XML sitemap generated with {len(processed_urls)} URLs")
    print("Sitemap saved to: website/sitemap.xml")

if __name__ == "__main__":
    generate_sitemap() 