import os
from bs4 import BeautifulSoup

def fix_bedford_duplicate():
    # Path to the Bedford page
    file_path = 'website/selfstoragebedfordshire/selfstoragebedford/index.html'
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all "About Storage in Bedford" sections
    about_sections = []
    for h2 in soup.find_all('h2'):
        if h2.text.strip() == 'About Storage in Bedford':
            # Get the parent div that contains the section
            parent_div = h2.parent
            if parent_div:
                about_sections.append(parent_div)
    
    # Check if we found multiple sections
    if len(about_sections) > 1:
        print(f"Found {len(about_sections)} 'About Storage in Bedford' sections")
        
        # Keep only the first section, remove the rest
        for section in about_sections[1:]:
            section.decompose()
        
        # Save the modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print("Successfully removed duplicate 'About Storage in Bedford' sections")
    else:
        print(f"No duplicate sections found. Found {len(about_sections)} 'About Storage in Bedford' section(s)")

if __name__ == "__main__":
    fix_bedford_duplicate() 