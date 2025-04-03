import os
import re
from bs4 import BeautifulSoup

def update_homepage():
    """
    Update the homepage with a new design while preserving search functionality
    """
    homepage_path = 'website/index.html'
    
    # Check if homepage exists
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage not found at {homepage_path}")
        return
    
    # Read the current homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get the script content (which contains the search functionality)
    script_content = ""
    for script in soup.find_all('script'):
        if script.string and 'function searchLocation()' in script.string:
            script_content = script.string
            break
    
    # Create the new homepage HTML structure
    new_html = """<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Self Storage Near Me | Find Local Storage Facilities</title>
<meta content="Find the best self storage facilities near you. Compare prices, amenities, and book online." name="description"/>
<link href="assets/css/style.css" rel="stylesheet"/>
<style>
    /* Additional styles for the redesigned homepage */
    .regions-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-top: 30px;
        margin-bottom: 50px;
    }
    
    .region-card {
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .region-card:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .region-card img {
        width: 100%;
        height: 150px;
        object-fit: cover;
    }
    
    .region-card-content {
        padding: 20px;
    }
    
    .region-card h3 {
        color: #006400;
        margin-bottom: 10px;
    }
    
    .region-card p {
        margin-bottom: 15px;
        color: #666;
    }
    
    .region-card .btn {
        display: inline-block;
        background-color: #28A745;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 500;
        transition: background-color 0.3s;
    }
    
    .region-card .btn:hover {
        background-color: #218838;
    }
    
    .text-boxes {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-top: 50px;
        margin-bottom: 50px;
    }
    
    .text-box {
        background-color: #f1f8e9;
        border-left: 4px solid #28A745;
        padding: 25px;
        border-radius: 6px;
    }
    
    .text-box h3 {
        color: #006400;
        margin-bottom: 15px;
    }
    
    .text-box p {
        color: #555;
    }
    
    .section-title {
        text-align: center;
        margin-top: 50px;
        margin-bottom: 20px;
        color: #006400;
        position: relative;
    }
    
    .section-title:after {
        content: "";
        display: block;
        width: 50px;
        height: 3px;
        background-color: #28A745;
        margin: 15px auto 0;
    }
    
    .browse-all {
        text-align: center;
        margin-top: 40px;
        margin-bottom: 50px;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .regions-grid, .text-boxes {
            grid-template-columns: 1fr;
        }
    }
</style>
</head>
<body>
<header>
<div class="container">
<div class="logo">Storage Finder</div>
<nav>
<ul>
<li><a href="index.html">Home</a></li>
<li><a href="selfstorageregions/index.html">Regions</a></li>
<li><a href="faq/index.html">FAQ</a></li>
<li><a href="about/index.html">About</a></li>
<li><a href="contact/index.html">Contact</a></li>
</ul>
</nav>
</div>
</header>
<div class="container">
<div class="hero">
<h1>Find Self Storage Near You</h1>
<p>Compare storage facilities and find the best deal for your needs.</p>
<div class="search-form"><input id="locationSearch" placeholder="Enter your location" style="padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px 0 0 4px; width: 70%;" type="text"/><button onclick="searchLocation()" style="padding: 12px 24px; background-color: #28A745; color: white; border: none; border-radius: 0 4px 4px 0; cursor: pointer; font-size: 16px;">Search</button></div>
</div>

<h2 class="section-title">Popular Storage Regions</h2>
<div class="regions-grid">
    <div class="region-card">
        <img src="assets/images/regions/devon.jpg" alt="Devon" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>Devon</h3>
            <p>23 cities, 45 facilities</p>
            <a href="selfstoragedevon/index.html" class="btn">View Region</a>
        </div>
    </div>
    
    <div class="region-card">
        <img src="assets/images/regions/greater-manchester.jpg" alt="Greater Manchester" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>Greater Manchester</h3>
            <p>37 cities, 120 facilities</p>
            <a href="selfstoragegreater-manchester/index.html" class="btn">View Region</a>
        </div>
    </div>
    
    <div class="region-card">
        <img src="assets/images/regions/west-yorkshire.jpg" alt="West Yorkshire" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>West Yorkshire</h3>
            <p>28 cities, 95 facilities</p>
            <a href="selfstoragewest-yorkshire/index.html" class="btn">View Region</a>
        </div>
    </div>
    
    <div class="region-card">
        <img src="assets/images/regions/north-yorkshire.jpg" alt="North Yorkshire" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>North Yorkshire</h3>
            <p>33 cities, 85 facilities</p>
            <a href="selfstoragenorth-yorkshire/index.html" class="btn">View Region</a>
        </div>
    </div>
    
    <div class="region-card">
        <img src="assets/images/regions/lincolnshire.jpg" alt="Lincolnshire" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>Lincolnshire</h3>
            <p>21 cities, 60 facilities</p>
            <a href="selfstoragelincolnshire/index.html" class="btn">View Region</a>
        </div>
    </div>
    
    <div class="region-card">
        <img src="assets/images/regions/kent.jpg" alt="Kent" onerror="this.src='assets/images/placeholder.jpg'">
        <div class="region-card-content">
            <h3>Kent</h3>
            <p>27 cities, 75 facilities</p>
            <a href="selfstoragekent/index.html" class="btn">View Region</a>
        </div>
    </div>
</div>

<h2 class="section-title">Why Choose Self Storage?</h2>
<div class="text-boxes">
    <div class="text-box">
        <h3>Secure Storage Solutions</h3>
        <p>Rest easy knowing your belongings are protected with top-tier security features at facilities across the UK.</p>
    </div>
    
    <div class="text-box">
        <h3>Flexible Options</h3>
        <p>From small lockers to large units, find the perfect size for your needs, whenever you need it.</p>
    </div>
    
    <div class="text-box">
        <h3>Local Convenience</h3>
        <p>Discover storage close to home with our extensive network of UK facilities.</p>
    </div>
</div>

<div class="browse-all">
    <a href="selfstorageregions/index.html" class="btn">Browse All Regions</a>
</div>

</div>
<footer><div class="container"><div class="footer-columns"><div class="footer-column"><h3>Legal</h3><ul><li><a href="privacy/index.html">Privacy Policy</a></li><li><a href="terms/index.html">Terms of Use</a></li><li><a href="membership/index.html">Membership Terms</a></li></ul></div><div class="footer-column"><h3>Navigate</h3><ul><li><a href="index.html">Home</a></li><li><a href="selfstorageregions/index.html">Regions</a></li><li><a href="faq/index.html">FAQ</a></li></ul></div><div class="footer-column"><h3>Company</h3><ul><li><a href="about/index.html">About Us</a></li><li><a href="contact/index.html">Contact</a></li></ul></div></div><div class="footer-bottom"><p>© 2024 Storage Finder. All rights reserved.</p></div></div></footer>
"""
    
    # Create the directory for placeholder images
    os.makedirs('website/assets/images', exist_ok=True)
    os.makedirs('website/assets/images/regions', exist_ok=True)
    
    # Create a placeholder image if it doesn't exist
    if not os.path.exists('website/assets/images/placeholder.jpg'):
        create_placeholder_image()
    
    # Combine the new HTML with the existing script for search functionality
    final_html = new_html + f"<script>{script_content}</script></body>\n</html>"
    
    # Save the updated homepage
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully updated the homepage with new design")

def create_placeholder_image():
    """Create a simple placeholder image"""
    try:
        # Create a basic placeholder image using HTML5 canvas
        placeholder_html = """
        <html>
        <body>
        <canvas id="canvas" width="400" height="250"></canvas>
        <script>
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        
        // Fill background
        ctx.fillStyle = '#e8f5e9';
        ctx.fillRect(0, 0, 400, 250);
        
        // Draw border
        ctx.strokeStyle = '#28A745';
        ctx.lineWidth = 10;
        ctx.strokeRect(5, 5, 390, 240);
        
        // Add text
        ctx.fillStyle = '#006400';
        ctx.font = '20px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Storage Region Image', 200, 125);
        
        // Convert to data URL and download
        var dataUrl = canvas.toDataURL('image/jpeg');
        var link = document.createElement('a');
        link.download = 'placeholder.jpg';
        link.href = dataUrl;
        link.click();
        </script>
        </body>
        </html>
        """
        
        with open('website/assets/images/placeholder.html', 'w') as f:
            f.write(placeholder_html)
        
        print("Created placeholder image generator HTML. Please open it in a browser to generate the placeholder.jpg")
        
        # For now, create a simple text file as a placeholder since we can't generate an actual image directly
        with open('website/assets/images/placeholder.jpg', 'w') as f:
            f.write("This is a placeholder for an image. Replace with an actual JPEG file.")
            
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

if __name__ == "__main__":
    update_homepage() 