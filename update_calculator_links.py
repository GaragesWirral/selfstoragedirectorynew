import os
import re

def update_calculator_links():
    """
    Updates the homepage to point calculator links to the dedicated calculator page
    """
    homepage_path = 'website/index.html'
    
    # Check if homepage exists
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage not found at {homepage_path}")
        return
    
    # Read the current homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the calculator link in the header
    # Find the calculator link in the navigation
    pattern = r'<li><a href="#calculator">Storage Calculator</a></li>'
    new_link = '<li><a href="calculator/index.html">Storage Calculator</a></li>'
    
    # Replace the link
    content = content.replace(pattern, new_link)
    
    # Save the updated homepage
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Successfully updated calculator links to point to the dedicated page!")

if __name__ == "__main__":
    update_calculator_links() 