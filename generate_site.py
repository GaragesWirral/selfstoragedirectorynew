import os
import pandas as pd
import zipfile
import shutil
from datetime import datetime

def generate_site():
    # ... existing code ...
    
    # Create website.zip
    with zipfile.ZipFile('website.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('website'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'website')
                zipf.write(file_path, arcname)
    
    # Unzip website.zip into website/ folder
    if os.path.exists('website'):
        shutil.rmtree('website')  # Remove existing website folder if it exists
    
    with zipfile.ZipFile('website.zip', 'r') as zipf:
        zipf.extractall('website')
    
    print("Site generation completed. Files are available in website.zip and website/ folder.")

if __name__ == "__main__":
    generate_site() 