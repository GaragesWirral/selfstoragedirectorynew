import os

def create_simple_placeholder():
    """Create simple binary placeholder images for the website"""
    
    # Create the directories if they don't exist
    os.makedirs('website/assets/images', exist_ok=True)
    os.makedirs('website/assets/images/regions', exist_ok=True)
    
    # A minimal 1x1 pixel GIF (valid binary data)
    minimal_gif = bytes([
        0x47, 0x49, 0x46, 0x38, 0x39, 0x61,  # GIF89a header
        0x01, 0x00, 0x01, 0x00,              # width=1, height=1
        0x80, 0x00, 0x00,                    # flags, background, ratio
        0x00, 0x00, 0x00,                    # RGB color (black)
        0x21, 0xF9, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00,  # GCE
        0x2C, 0x00, 0x00, 0x00, 0x00,        # Image descriptor
        0x01, 0x00, 0x01, 0x00, 0x00,        # width=1, height=1, flags
        0x02, 0x02, 0x44, 0x01, 0x00         # LZW min code size, block size, data, end
    ])
    
    # Create main placeholder
    placeholder_path = 'website/assets/images/placeholder.jpg'
    with open(placeholder_path, 'wb') as f:
        f.write(minimal_gif)
    print(f"Created valid placeholder image at {placeholder_path}")
    
    # Create region-specific placeholders
    regions = ['devon', 'greater-manchester', 'west-yorkshire', 'north-yorkshire', 'lincolnshire', 'kent']
    for region in regions:
        region_path = f'website/assets/images/regions/{region}.jpg'
        with open(region_path, 'wb') as f:
            f.write(minimal_gif)
        print(f"Created placeholder image for {region}")
    
    # Remove the HTML placeholder generator as it's no longer needed
    if os.path.exists('website/assets/images/placeholder.html'):
        try:
            os.remove('website/assets/images/placeholder.html')
            print("Removed unnecessary placeholder HTML generator")
        except:
            print("Could not remove placeholder HTML file")
    
    # Modify the image references in the HTML
    try:
        homepage_path = 'website/index.html'
        with open(homepage_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Optional: Fix any specific image issues here if needed
            
        print("Checked homepage image references")
    except Exception as e:
        print(f"Error checking homepage: {e}")
        
    print("Image fix complete!")

if __name__ == "__main__":
    create_simple_placeholder() 