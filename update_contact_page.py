import os
import re

def update_contact_page():
    """
    Updates the contact page with correct contact information and removes address/business hours
    """
    contact_page = 'website/contact/index.html'
    
    # Read the current content
    with open(contact_page, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace all instances of contact information
    replacements = {
        'info@storagefinder.co.uk': 'support@storagefinder.uk',
        'support@storagefinder.co.uk': 'support@storagefinder.uk',
        'contact@storagefinder.uk': 'support@storagefinder.uk',
        'partners@storagefinder.co.uk': 'support@storagefinder.uk',
        '020 1234 5678': '07519667044',
        '020 1234 5679': '07519667044',
        '020 7123 4567': '07519667044',
        'tel:+4402012345678': 'tel:+447519667044',
        'tel:+4402012345679': 'tel:+447519667044'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Update the contact info section to only show email and phone
    new_contact_section = '''<div class="contact-info">
<h2>Get in Touch</h2>
<div class="contact-method">
<h3>
<svg fill="none" height="20" viewbox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg">
<path d="M20 4H4C2.9 4 2 4.9 2 6V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4Z" stroke="#006400" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
<path d="M22 6L12 13L2 6" stroke="#006400" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
                Email
            </h3>
<p><a href="mailto:support@storagefinder.uk">support@storagefinder.uk</a></p>
</div>
<div class="contact-method">
<h3>
<svg fill="none" height="20" viewbox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg">
<path d="M22 16.92V19.92C22 20.4704 21.7893 20.9983 21.4142 21.3734C21.0391 21.7485 20.5113 21.9592 19.96 21.96C16.4194 21.6225 13.0269 20.3923 10.07 18.38C7.34382 16.5644 5.04467 14.2653 3.22999 11.54C1.21 8.57003 0.979994 5.16003 0.659994 1.61003C0.664301 1.06107 0.875081 0.536007 1.24932 0.162233C1.62357 -0.211541 2.14955 -0.420583 2.69999 -0.410027H5.69999C6.72671 -0.422966 7.56286 0.359843 7.68999 1.37003C7.81097 2.5001 8.04166 3.61402 8.37999 4.69003C8.66383 5.55203 8.42626 6.51609 7.76999 7.20003L6.49999 8.47003C8.17147 11.3119 10.6281 13.7685 13.47 15.44L14.74 14.17C15.4239 13.5137 16.388 13.2761 17.25 13.56C18.326 13.8983 19.4399 14.129 20.57 14.25C21.598 14.38 22.3907 15.2387 22.36 16.28L22 16.92Z" stroke="#006400" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
                Phone
            </h3>
<p><a href="tel:+447519667044">07519667044</a></p>
</div>
</div>'''
    
    # Replace the entire contact info section using regex
    content = re.sub(
        r'<div class="contact-info">.*?<div class="about-section">',
        new_contact_section + '</div>\n<div class="about-section">',
        content,
        flags=re.DOTALL
    )
    
    # Update the facility owners section
    content = re.sub(
        r'<div class="about-section">.*?</div>\s*</div>\s*</div>',
        '''<div class="about-section">
<h2>Facility Owners & Partners</h2>
<p>If you own or manage a self storage facility and would like to be listed on our directory, please contact us at <a href="mailto:support@storagefinder.uk">support@storagefinder.uk</a> or call <a href="tel:+447519667044">07519667044</a> to discuss our listing options and marketing opportunities.</p>
</div></div></div>''',
        content,
        flags=re.DOTALL
    )
    
    # Write the updated content back to the file
    with open(contact_page, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Contact page updated successfully")

if __name__ == "__main__":
    update_contact_page() 