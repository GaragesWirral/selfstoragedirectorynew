import os
import re
from bs4 import BeautifulSoup
import time

def update_homepage():
    with open('website/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Add container div to header
    header = soup.header
    if header and not header.find('div', class_='container'):
        container = soup.new_tag('div', attrs={'class': 'container'})
        for child in list(header.children):
            container.append(child.extract())
        header.append(container)
    
    # Replace main with container div
    main = soup.main
    if main:
        container = soup.new_tag('div', attrs={'class': 'container'})
        for child in list(main.children):
            container.append(child.extract())
        main.replace_with(container)
    
    # Update hero section
    hero = soup.find('section', class_='hero')
    if hero:
        div_hero = soup.new_tag('div', attrs={'class': 'hero'})
        for child in list(hero.children):
            div_hero.append(child.extract())
        hero.replace_with(div_hero)
    
    # Update form to search-form
    form = soup.find('form')
    if form:
        search_form = soup.new_tag('div', attrs={'class': 'search-form'})
        input_tag = soup.new_tag('input', attrs={
            'type': 'text', 
            'id': 'locationSearch', 
            'placeholder': 'Enter your location'
        })
        button = soup.new_tag('button', attrs={'onclick': 'searchLocation()'})
        button.string = 'Search'
        search_form.append(input_tag)
        search_form.append(button)
        form.replace_with(search_form)
    
    # Update regions grid to list
    regions_grid = soup.find('div', class_='regions-grid')
    if regions_grid:
        regions_list = soup.new_tag('div', attrs={'class': 'regions-list'})
        for child in list(regions_grid.children):
            regions_list.append(child.extract())
        regions_grid.replace_with(regions_list)
    
    # Update footer
    footer = soup.footer
    if footer:
        container = soup.new_tag('div', attrs={'class': 'container'})
        footer_columns = soup.new_tag('div', attrs={'class': 'footer-columns'})
        
        # Legal column
        legal_column = soup.new_tag('div', attrs={'class': 'footer-column'})
        legal_title = soup.new_tag('h3')
        legal_title.string = 'Legal'
        legal_column.append(legal_title)
        
        legal_list = soup.new_tag('ul')
        for link in [('Privacy Policy', 'privacy/index.html'), 
                    ('Terms of Use', 'terms/index.html'),
                    ('Membership Terms', 'membership/index.html')]:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=link[1])
            a.string = link[0]
            li.append(a)
            legal_list.append(li)
        
        legal_column.append(legal_list)
        footer_columns.append(legal_column)
        
        # Navigate column
        nav_column = soup.new_tag('div', attrs={'class': 'footer-column'})
        nav_title = soup.new_tag('h3')
        nav_title.string = 'Navigate'
        nav_column.append(nav_title)
        
        nav_list = soup.new_tag('ul')
        for link in [('Home', 'index.html'), 
                    ('Regions', 'selfstorageregions/index.html'),
                    ('FAQ', 'faq/index.html')]:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=link[1])
            a.string = link[0]
            li.append(a)
            nav_list.append(li)
        
        nav_column.append(nav_list)
        footer_columns.append(nav_column)
        
        # Company column
        company_column = soup.new_tag('div', attrs={'class': 'footer-column'})
        company_title = soup.new_tag('h3')
        company_title.string = 'Company'
        company_column.append(company_title)
        
        company_list = soup.new_tag('ul')
        for link in [('About Us', 'about/index.html'), 
                    ('Contact', 'contact/index.html')]:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=link[1])
            a.string = link[0]
            li.append(a)
            company_list.append(li)
        
        company_column.append(company_list)
        footer_columns.append(company_column)
        
        # Footer bottom
        footer_bottom = soup.new_tag('div', attrs={'class': 'footer-bottom'})
        copyright = soup.new_tag('p')
        copyright.string = '© 2024 Storage Finder. All rights reserved.'
        footer_bottom.append(copyright)
        
        # Clear and rebuild footer
        footer.clear()
        container.append(footer_columns)
        container.append(footer_bottom)
        footer.append(container)
    
    # Add search script
    script = soup.new_tag('script')
    script.string = """
function searchLocation() {
    var input = document.getElementById('locationSearch').value.toLowerCase();
    if (input.trim() === '') {
        alert('Please enter a location to search for');
        return;
    }
    
    // Redirect to regions page with search query
    window.location.href = 'selfstorageregions/index.html?search=' + encodeURIComponent(input);
}
"""
    soup.body.append(script)
    
    # Save updated file
    with open('website/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Updated homepage")

def update_region_pages():
    for region_dir in os.listdir('website'):
        if not region_dir.startswith('selfstorage') or not os.path.isdir(os.path.join('website', region_dir)):
            continue
        
        region_page = os.path.join('website', region_dir, 'index.html')
        if not os.path.exists(region_page):
            continue
        
        region_name = region_dir.replace('selfstorage', '')
        print(f"Updating region page: {region_name}")
        
        with open(region_page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add container div to header
        header = soup.header
        if header and not header.find('div', class_='container'):
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(header.children):
                container.append(child.extract())
            header.append(container)
        
        # Get the body content container
        body_container = None
        main = soup.main
        if main:
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(main.children):
                container.append(child.extract())
            main.replace_with(container)
            body_container = container
        elif not soup.find('div', class_='container', recursive=False):
            # If no main or container, wrap content
            body = soup.body
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(body.children):
                if child.name != 'header' and child.name != 'footer' and child.name != 'script':
                    container.append(child.extract())
            header.insert_after(container)
            body_container = container
        else:
            body_container = soup.find('div', class_='container', recursive=False)
        
        # Add breadcrumbs if they don't exist
        if body_container and not body_container.find('div', class_='breadcrumbs'):
            h1 = body_container.find('h1')
            if h1:
                breadcrumbs = soup.new_tag('div', attrs={'class': 'breadcrumbs'})
                home_link = soup.new_tag('a', href='../index.html')
                home_link.string = 'Home'
                regions_link = soup.new_tag('a', href='../selfstorageregions/index.html')
                regions_link.string = 'Regions'
                region_span = soup.new_tag('span')
                region_span.string = region_name.replace('-', ' ').title()
                
                breadcrumbs.append(home_link)
                breadcrumbs.append(' > ')
                breadcrumbs.append(regions_link)
                breadcrumbs.append(' > ')
                breadcrumbs.append(region_span)
                
                h1.insert_before(breadcrumbs)
        
        # Wrap region intro content
        if body_container:
            h1 = body_container.find('h1')
            if h1 and h1.find_next_sibling('p'):
                p = h1.find_next_sibling('p')
                region_intro = soup.new_tag('div', attrs={'class': 'region-intro'})
                
                # Move breadcrumbs inside region-intro if they exist
                breadcrumbs = body_container.find('div', class_='breadcrumbs')
                if breadcrumbs:
                    region_intro.append(breadcrumbs.extract())
                
                region_intro.append(h1.extract())
                region_intro.append(p.extract())
                
                body_container.insert(0, region_intro)
        
        # Add search form
        if body_container and not body_container.find('div', class_='search-form'):
            search_form = soup.new_tag('div', attrs={'class': 'search-form'})
            input_tag = soup.new_tag('input', attrs={
                'type': 'text', 
                'id': 'citySearch', 
                'placeholder': f'Search for a city in {region_name.replace("-", " ").title()}...'
            })
            button = soup.new_tag('button', attrs={'onclick': 'searchCity()'})
            button.string = 'Search'
            search_form.append(input_tag)
            search_form.append(button)
            
            region_intro = body_container.find('div', class_='region-intro')
            if region_intro:
                region_intro.insert_after(search_form)
            else:
                body_container.insert(0, search_form)
            
            # Add search results heading
            results_heading = soup.new_tag('h2', attrs={'id': 'search-results-heading'})
            results_heading.string = f'Cities with Self Storage in {region_name.replace("-", " ").title()}'
            search_form.insert_after(results_heading)
        
        # Convert cities list to city cards grid
        cities_list = body_container.find('ul') if body_container else None
        cities_grid = None
        if cities_list:
            cities_grid = soup.new_tag('div', attrs={'class': 'cities-grid'})
            for li in cities_list.find_all('li', recursive=False):
                a = li.find('a')
                if a:
                    city_name = a.string
                    city_card = soup.new_tag('div', attrs={'class': 'city-card'})
                    h3 = soup.new_tag('h3')
                    h3.string = city_name
                    p = soup.new_tag('p')
                    p.string = '1 Storage Facility'  # Default value, could be customized
                    btn = soup.new_tag('a', attrs={'href': a['href']})
                    btn.string = 'View Storage Options'
                    
                    city_card.append(h3)
                    city_card.append(p)
                    city_card.append(btn)
                    cities_grid.append(city_card)
            
            cities_list.replace_with(cities_grid)
        
        # Replace any existing region-list with cities-grid
        region_list = body_container.find('div', class_='regions-list') if body_container else None
        if region_list and not cities_grid:
            cities_grid = soup.new_tag('div', attrs={'class': 'cities-grid'})
            for card in region_list.find_all('div', class_='region-card'):
                city_card = soup.new_tag('div', attrs={'class': 'city-card'})
                
                h3 = card.find('h3')
                if h3:
                    new_h3 = soup.new_tag('h3')
                    new_h3.string = h3.string
                    city_card.append(new_h3)
                
                p = card.find('p')
                if p:
                    new_p = soup.new_tag('p')
                    new_p.string = p.string
                    city_card.append(new_p)
                
                a = card.find('a', class_='btn')
                if a:
                    new_a = soup.new_tag('a', href=a['href'])
                    new_a.string = 'View Storage Options'
                    city_card.append(new_a)
                
                cities_grid.append(city_card)
            
            region_list.replace_with(cities_grid)
        
        # Update footer
        footer = soup.footer
        if footer:
            container = soup.new_tag('div', attrs={'class': 'container'})
            footer_columns = soup.new_tag('div', attrs={'class': 'footer-columns'})
            
            # Determine relative path
            rel_path = "../"
            
            # Legal column
            legal_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            legal_title = soup.new_tag('h3')
            legal_title.string = 'Legal'
            legal_column.append(legal_title)
            
            legal_list = soup.new_tag('ul')
            for link in [('Privacy Policy', f'{rel_path}privacy/index.html'), 
                         ('Terms of Use', f'{rel_path}terms/index.html'),
                         ('Membership Terms', f'{rel_path}membership/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                legal_list.append(li)
            
            legal_column.append(legal_list)
            footer_columns.append(legal_column)
            
            # Navigate column
            nav_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            nav_title = soup.new_tag('h3')
            nav_title.string = 'Navigate'
            nav_column.append(nav_title)
            
            nav_list = soup.new_tag('ul')
            for link in [('Home', f'{rel_path}index.html'), 
                         ('Regions', f'{rel_path}selfstorageregions/index.html'),
                         ('FAQ', f'{rel_path}faq/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                nav_list.append(li)
            
            nav_column.append(nav_list)
            footer_columns.append(nav_column)
            
            # Company column
            company_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            company_title = soup.new_tag('h3')
            company_title.string = 'Company'
            company_column.append(company_title)
            
            company_list = soup.new_tag('ul')
            for link in [('About Us', f'{rel_path}about/index.html'), 
                         ('Contact', f'{rel_path}contact/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                company_list.append(li)
            
            company_column.append(company_list)
            footer_columns.append(company_column)
            
            # Footer bottom
            footer_bottom = soup.new_tag('div', attrs={'class': 'footer-bottom'})
            copyright = soup.new_tag('p')
            copyright.string = '© 2024 Storage Finder. All rights reserved.'
            footer_bottom.append(copyright)
            
            container.append(footer_columns)
            container.append(footer_bottom)
            
            # Replace footer content
            footer.clear()
            footer.append(container)
        
        # Add search script
        script_found = False
        for script in soup.find_all('script'):
            if script.string and 'searchCity' in script.string:
                script_found = True
                # Update the script to work with city-cards
                script.string = """
function searchCity() {
    var input = document.getElementById('citySearch').value.toLowerCase();
    var cards = document.querySelectorAll('.city-card');
    var resultsHeading = document.getElementById('search-results-heading');
    var foundCount = 0;
    
    cards.forEach(function(card) {
        var cityName = card.querySelector('h3').innerText.toLowerCase();
        
        if (cityName.includes(input)) {
            card.style.display = 'block';
            foundCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    if (input === '') {
        resultsHeading.innerText = 'Cities with Self Storage in """ + region_name.replace('-', ' ').title() + """';
    } else if (foundCount === 0) {
        resultsHeading.innerText = 'No cities found matching "' + input + '"';
    } else {
        resultsHeading.innerText = 'Cities matching "' + input + '"';
    }
}
"""
                break
        
        if not script_found:
            script = soup.new_tag('script')
            script.string = """
function searchCity() {
    var input = document.getElementById('citySearch').value.toLowerCase();
    var cards = document.querySelectorAll('.city-card');
    var resultsHeading = document.getElementById('search-results-heading');
    var foundCount = 0;
    
    cards.forEach(function(card) {
        var cityName = card.querySelector('h3').innerText.toLowerCase();
        
        if (cityName.includes(input)) {
            card.style.display = 'block';
            foundCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    if (input === '') {
        resultsHeading.innerText = 'Cities with Self Storage in """ + region_name.replace('-', ' ').title() + """';
    } else if (foundCount === 0) {
        resultsHeading.innerText = 'No cities found matching "' + input + '"';
    } else {
        resultsHeading.innerText = 'Cities matching "' + input + '"';
    }
}
"""
            soup.body.append(script)
        
        # Save updated file
        with open(region_page, 'w', encoding='utf-8') as f:
            f.write(str(soup))

def update_city_pages():
    for region_dir in os.listdir('website'):
        if not region_dir.startswith('selfstorage') or not os.path.isdir(os.path.join('website', region_dir)):
            continue
        
        for city_dir in os.listdir(os.path.join('website', region_dir)):
            if not city_dir.startswith('selfstorage') or not os.path.isdir(os.path.join('website', region_dir, city_dir)):
                continue
            
            city_page = os.path.join('website', region_dir, city_dir, 'index.html')
            if not os.path.exists(city_page):
                continue
            
            with open(city_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Add container div to header
            header = soup.header
            if header and not header.find('div', class_='container'):
                container = soup.new_tag('div', attrs={'class': 'container'})
                for child in list(header.children):
                    container.append(child.extract())
                header.append(container)
            
            # Replace main with container div
            main = soup.main
            if main:
                container = soup.new_tag('div', attrs={'class': 'container'})
                for child in list(main.children):
                    container.append(child.extract())
                main.replace_with(container)
            elif not soup.find('div', class_='container', recursive=False):
                # If no main or container, wrap content
                body = soup.body
                container = soup.new_tag('div', attrs={'class': 'container'})
                for child in list(body.children):
                    if child.name != 'header' and child.name != 'footer' and child.name != 'script':
                        container.append(child.extract())
                header.insert_after(container)
            
            # Update provider list to storage list
            provider_list = soup.find('div', class_='provider-list')
            if provider_list:
                storage_list = soup.new_tag('div', attrs={'class': 'storage-list'})
                
                for provider in provider_list.find_all('div', class_='provider'):
                    storage_card = soup.new_tag('div', attrs={'class': 'storage-card'})
                    
                    # Move the h3 title
                    h3 = provider.find('h3')
                    if h3:
                        storage_card.append(h3.extract())
                    
                    # Create storage info div
                    storage_info = soup.new_tag('div', attrs={'class': 'storage-info'})
                    
                    # Process address
                    address_p = provider.find('p')
                    if address_p:
                        address_new = soup.new_tag('p')
                        strong = soup.new_tag('strong')
                        strong.string = 'Address: '
                        address_new.append(strong)
                        address_new.append(address_p.get_text())
                        storage_info.append(address_new)
                    
                    # Create contact info div
                    contact_info = soup.new_tag('div', attrs={'class': 'contact-info'})
                    
                    # Process phone
                    phone_p = provider.find_all('p')[1] if len(provider.find_all('p')) > 1 else None
                    if phone_p and 'Phone' in phone_p.get_text():
                        phone_new = soup.new_tag('p')
                        strong = soup.new_tag('strong')
                        strong.string = 'Phone: '
                        phone_new.append(strong)
                        
                        phone_num = re.search(r'[\d\-]+', phone_p.get_text())
                        if phone_num:
                            phone_link = soup.new_tag('a', href=f"tel:{phone_num.group().replace('-', '')}")
                            phone_link.string = phone_num.group()
                            phone_new.append(phone_link)
                            contact_info.append(phone_new)
                    
                    # Process website
                    website_p = provider.find_all('p')[2] if len(provider.find_all('p')) > 2 else None
                    if website_p and 'Website' in website_p.get_text():
                        website_new = soup.new_tag('p')
                        strong = soup.new_tag('strong')
                        strong.string = 'Website: '
                        website_new.append(strong)
                        
                        website_link = website_p.find('a')
                        if website_link:
                            new_link = soup.new_tag('a', href=website_link['href'], target='_blank')
                            new_link.string = website_link.string
                            website_new.append(new_link)
                            contact_info.append(website_new)
                    
                    storage_info.append(contact_info)
                    storage_card.append(storage_info)
                    storage_list.append(storage_card)
                
                provider_list.replace_with(storage_list)
            
            # Update footer
            footer = soup.footer
            if footer:
                container = soup.new_tag('div', attrs={'class': 'container'})
                footer_columns = soup.new_tag('div', attrs={'class': 'footer-columns'})
                
                # Determine relative path
                rel_path = "../../"
                
                # Legal column
                legal_column = soup.new_tag('div', attrs={'class': 'footer-column'})
                legal_title = soup.new_tag('h3')
                legal_title.string = 'Legal'
                legal_column.append(legal_title)
                
                legal_list = soup.new_tag('ul')
                for link in [('Privacy Policy', f'{rel_path}privacy/index.html'), 
                            ('Terms of Use', f'{rel_path}terms/index.html'),
                            ('Membership Terms', f'{rel_path}membership/index.html')]:
                    li = soup.new_tag('li')
                    a = soup.new_tag('a', href=link[1])
                    a.string = link[0]
                    li.append(a)
                    legal_list.append(li)
                
                legal_column.append(legal_list)
                footer_columns.append(legal_column)
                
                # Navigate column
                nav_column = soup.new_tag('div', attrs={'class': 'footer-column'})
                nav_title = soup.new_tag('h3')
                nav_title.string = 'Navigate'
                nav_column.append(nav_title)
                
                nav_list = soup.new_tag('ul')
                for link in [('Home', f'{rel_path}index.html'), 
                            ('Regions', f'{rel_path}selfstorageregions/index.html'),
                            ('FAQ', f'{rel_path}faq/index.html')]:
                    li = soup.new_tag('li')
                    a = soup.new_tag('a', href=link[1])
                    a.string = link[0]
                    li.append(a)
                    nav_list.append(li)
                
                nav_column.append(nav_list)
                footer_columns.append(nav_column)
                
                # Company column
                company_column = soup.new_tag('div', attrs={'class': 'footer-column'})
                company_title = soup.new_tag('h3')
                company_title.string = 'Company'
                company_column.append(company_title)
                
                company_list = soup.new_tag('ul')
                for link in [('About Us', f'{rel_path}about/index.html'), 
                            ('Contact', f'{rel_path}contact/index.html')]:
                    li = soup.new_tag('li')
                    a = soup.new_tag('a', href=link[1])
                    a.string = link[0]
                    li.append(a)
                    company_list.append(li)
                
                company_column.append(company_list)
                footer_columns.append(company_column)
                
                # Footer bottom
                footer_bottom = soup.new_tag('div', attrs={'class': 'footer-bottom'})
                copyright = soup.new_tag('p')
                copyright.string = '© 2024 Storage Finder. All rights reserved.'
                footer_bottom.append(copyright)
                
                # Clear and rebuild footer
                footer.clear()
                container.append(footer_columns)
                container.append(footer_bottom)
                footer.append(container)
            
            # Save updated file
            with open(city_page, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated city page: {region_dir}/{city_dir}")

def update_top_level_pages():
    for page_dir in ['about', 'contact', 'faq', 'privacy', 'terms', 'membership', 'selfstorageregions']:
        page_path = os.path.join('website', page_dir, 'index.html')
        if not os.path.exists(page_path):
            continue
        
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add container div to header
        header = soup.header
        if header and not header.find('div', class_='container'):
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(header.children):
                container.append(child.extract())
            header.append(container)
        
        # Replace main with container div
        main = soup.main
        if main:
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(main.children):
                container.append(child.extract())
            main.replace_with(container)
        elif not soup.find('div', class_='container', recursive=False):
            # If no main or container, wrap content
            body = soup.body
            container = soup.new_tag('div', attrs={'class': 'container'})
            for child in list(body.children):
                if child.name != 'header' and child.name != 'footer' and child.name != 'script':
                    container.append(child.extract())
            header.insert_after(container)
        
        # Update footer
        footer = soup.footer
        if footer:
            container = soup.new_tag('div', attrs={'class': 'container'})
            footer_columns = soup.new_tag('div', attrs={'class': 'footer-columns'})
            
            # Determine relative path
            rel_path = "../"
            
            # Legal column
            legal_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            legal_title = soup.new_tag('h3')
            legal_title.string = 'Legal'
            legal_column.append(legal_title)
            
            legal_list = soup.new_tag('ul')
            for link in [('Privacy Policy', f'{rel_path}privacy/index.html'), 
                        ('Terms of Use', f'{rel_path}terms/index.html'),
                        ('Membership Terms', f'{rel_path}membership/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                legal_list.append(li)
            
            legal_column.append(legal_list)
            footer_columns.append(legal_column)
            
            # Navigate column
            nav_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            nav_title = soup.new_tag('h3')
            nav_title.string = 'Navigate'
            nav_column.append(nav_title)
            
            nav_list = soup.new_tag('ul')
            for link in [('Home', f'{rel_path}index.html'), 
                        ('Regions', f'{rel_path}selfstorageregions/index.html'),
                        ('FAQ', f'{rel_path}faq/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                nav_list.append(li)
            
            nav_column.append(nav_list)
            footer_columns.append(nav_column)
            
            # Company column
            company_column = soup.new_tag('div', attrs={'class': 'footer-column'})
            company_title = soup.new_tag('h3')
            company_title.string = 'Company'
            company_column.append(company_title)
            
            company_list = soup.new_tag('ul')
            for link in [('About Us', f'{rel_path}about/index.html'), 
                        ('Contact', f'{rel_path}contact/index.html')]:
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=link[1])
                a.string = link[0]
                li.append(a)
                company_list.append(li)
            
            company_column.append(company_list)
            footer_columns.append(company_column)
            
            # Footer bottom
            footer_bottom = soup.new_tag('div', attrs={'class': 'footer-bottom'})
            copyright = soup.new_tag('p')
            copyright.string = '© 2024 Storage Finder. All rights reserved.'
            footer_bottom.append(copyright)
            
            # Clear and rebuild footer
            footer.clear()
            container.append(footer_columns)
            container.append(footer_bottom)
            footer.append(container)
        
        # Save updated file
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated page: {page_dir}")

if __name__ == "__main__":
    print("Starting website enhancement...")
    update_homepage()
    update_region_pages()
    update_city_pages()
    update_top_level_pages()
    print("Website enhancement complete!") 