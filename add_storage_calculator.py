import os
import re

def add_storage_calculator():
    """
    Updates the homepage to add a storage size calculator and adds a link in the header
    """
    homepage_path = 'website/index.html'
    
    # Check if homepage exists
    if not os.path.exists(homepage_path):
        print(f"Error: Homepage not found at {homepage_path}")
        return
    
    # Read the current homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add the calculator link to the header
    nav_pattern = r'<nav>\s*<ul>(.*?)</ul>\s*</nav>'
    nav_content = re.search(nav_pattern, content, re.DOTALL).group(1)
    
    # Check if calculator link already exists
    if 'calculator' not in nav_content.lower():
        new_nav_content = nav_content + '\n<li><a href="#calculator">Storage Calculator</a></li>'
        content = content.replace(nav_content, new_nav_content)
        print("Added calculator link to header navigation")
    
    # 2. Add the calculator section to the page
    # Look for the popular regions section to place our calculator before it
    regions_section_start = content.find('<h2 class="section-title">Popular Storage Regions</h2>')
    
    if regions_section_start != -1:
        # HTML for the calculator section
        calculator_html = '''
<div id="calculator" class="calculator-section">
    <h2 class="section-title">Find Your Perfect Storage Size</h2>
    <div class="calculator-container">
        <form onsubmit="return calculateStorageSize()">
            <div class="calculator-grid">
                <div class="calculator-item">
                    <label for="calc-boxes">Boxes:</label>
                    <select id="calc-boxes" name="boxes">
                        <option value="none">None</option>
                        <option value="few">Few (1-5)</option>
                        <option value="several">Several (6-15)</option>
                        <option value="many">Many (16+)</option>
                    </select>
                </div>
                
                <div class="calculator-item">
                    <label for="calc-furniture">Furniture:</label>
                    <select id="calc-furniture" name="furniture">
                        <option value="none">None</option>
                        <option value="small">Small (e.g., chair, table)</option>
                        <option value="medium">Medium (e.g., sofa, bed)</option>
                        <option value="large">Large (multiple rooms)</option>
                    </select>
                </div>
                
                <div class="calculator-item">
                    <label for="calc-appliances">Appliances:</label>
                    <select id="calc-appliances" name="appliances">
                        <option value="none">None</option>
                        <option value="small">Small (e.g., microwave)</option>
                        <option value="large">Large (e.g., fridge, washer)</option>
                    </select>
                </div>
                
                <div class="calculator-item">
                    <label for="calc-electronics">Electronics:</label>
                    <select id="calc-electronics" name="electronics">
                        <option value="none">None</option>
                        <option value="some">Some (e.g., TV, computer)</option>
                        <option value="many">Many (multiple devices)</option>
                    </select>
                </div>
            </div>
            
            <div class="calculator-submit">
                <button type="submit" class="calc-button">Calculate Size</button>
            </div>
        </form>
        
        <div id="calculator-result" style="display:none;"></div>
    </div>
</div>
'''

        # Add the calculator CSS
        calculator_css = '''
    /* Storage Calculator Styles */
    .calculator-section {
        margin: 50px 0;
        padding: 30px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .calculator-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .calculator-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .calculator-item {
        margin-bottom: 15px;
    }
    
    .calculator-item label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #006400;
    }
    
    .calculator-item select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 16px;
    }
    
    .calculator-submit {
        text-align: center;
    }
    
    .calc-button {
        background-color: #28A745;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .calc-button:hover {
        background-color: #218838;
    }
    
    .result-box {
        margin-top: 30px;
        padding: 20px;
        background-color: #e8f5e9;
        border-left: 4px solid #28A745;
        border-radius: 4px;
    }
    
    .result-box h3 {
        color: #006400;
        margin-bottom: 10px;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .calculator-grid {
            grid-template-columns: 1fr;
        }
    }
'''

        # Insert the calculator CSS into the <style> section
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + calculator_css + content[style_end:]
            print("Added calculator CSS to the style section")
        
        # Insert the calculator HTML before the popular regions section
        content = content[:regions_section_start] + calculator_html + content[regions_section_start:]
        print("Added calculator HTML section to the homepage")
        
        # 3. Add the JavaScript file reference to the <head> section
        head_end = content.find('</head>')
        if head_end != -1:
            js_script_tag = '<script src="assets/js/storage-calculator.js"></script>\n'
            content = content[:head_end] + js_script_tag + content[head_end:]
            print("Added JavaScript file reference to the head section")
        
        # Save the updated homepage
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Successfully updated the homepage with the storage calculator!")
    else:
        print("Error: Could not find the popular regions section in the homepage")

if __name__ == "__main__":
    add_storage_calculator() 