import os
from bs4 import BeautifulSoup

def fix_bradford_content():
    """Fix remaining issues in Bradford page content."""
    # Path to Bradford HTML file
    bradford_html_path = 'website/selfstoragewest-yorkshire/selfstoragebradford/index.html'
    
    # Check if the file exists
    if not os.path.exists(bradford_html_path):
        print(f"Bradford HTML file not found: {bradford_html_path}")
        return
    
    # Read the Bradford HTML file
    with open(bradford_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Update the paragraph text
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        if 'Leeds' in p.text:
            p.string = p.text.replace('Leeds', 'Bradford')
    
    # Update breadcrumbs
    span_tags = soup.find_all('span')
    for span in span_tags:
        if span.text == 'Leeds':
            span.string = 'Bradford'
    
    # Save the updated file
    with open(bradford_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("Successfully fixed remaining Leeds references in Bradford page")

if __name__ == "__main__":
    fix_bradford_content() 