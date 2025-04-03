import os
import re
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Verify website structure")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("--check-links", action="store_true", help="Check for broken links")
    return parser.parse_args()

def check_html_file(filepath, check_links=False, verbose=False):
    """Check HTML file for various issues."""
    issues = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check title
        title = soup.find('title')
        if not title:
            issues.append("Missing title")
        elif len(title.text.strip()) < 10:
            warnings.append(f"Very short title: {title.text.strip()}")
        
        # Check meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            warnings.append("Missing meta description")
        elif 'content' not in meta_desc.attrs:
            warnings.append("Meta description has no content attribute")
        elif len(meta_desc['content']) < 50:
            warnings.append(f"Very short meta description: {meta_desc['content']}")
        
        # Check for placeholder content
        example_patterns = [
            r'example storage', r'sample facility', r'placeholder', 
            r'john doe', r'jane smith', r'test storage', 
            r'demo storage', r'123-?456-?7890', r'www\.example\.com'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"Contains placeholder content: {matches[0]}")
                break
        
        # Check navigation
        nav = soup.find('nav')
        if not nav:
            warnings.append("Missing navigation")
        else:
            nav_links = nav.find_all('a')
            if len(nav_links) < 3:
                warnings.append(f"Navigation has only {len(nav_links)} links")
        
        # Check for broken images
        img_tags = soup.find_all('img')
        for img in img_tags:
            if 'src' not in img.attrs or not img['src'] or img['src'] == '#':
                warnings.append(f"Broken image: {img}")
            if 'alt' not in img.attrs or not img['alt']:
                warnings.append("Image missing alt text")
        
        # Check for empty containers
        for cls in ['storage-list', 'main-content', 'footer-content']:
            elem = soup.find(class_=cls)
            if elem and len(elem.get_text(strip=True)) < 10:
                issues.append(f"Empty {cls} container")
        
        # Check if this is a city page and if it has a storage-list section
        parts = filepath.split(os.sep)
        is_city_page = False
        
        # Check the path pattern for city pages
        if len(parts) > 3 and parts[-1] == "index.html":
            parent_dir = parts[-2]
            if parent_dir.startswith("selfstorage"):
                is_city_page = True
        
        if is_city_page:
            main_content = soup.find('main')
            if main_content:
                storage_list = main_content.find(class_="storage-list")
                if not storage_list:
                    issues.append("Missing storage-list container in city page")
        
        # Check if this is a region page and if it has a storage-list section
        is_region_page = False
        if len(parts) > 2 and parts[-1] == "index.html":
            if parts[-2].startswith("selfstorage") and "self" not in parts[-3].lower():
                is_region_page = True
        
        if is_region_page:
            main_content = soup.find('main')
            if main_content:
                storage_list = main_content.find(class_="storage-list")
                if not storage_list:
                    issues.append("Missing storage-list container in region page")
        
        # Check links if requested
        if check_links:
            links = soup.find_all('a')
            for link in links:
                if 'href' not in link.attrs:
                    warnings.append("Link missing href attribute")
                elif link['href'] == '#' or link['href'] == '':
                    warnings.append("Empty link")
        
        if verbose and (issues or warnings):
            print(f"Checked {filepath}")
            if issues:
                print(f"  Issues: {', '.join(issues)}")
            if warnings:
                print(f"  Warnings: {', '.join(warnings)}")
        
        return filepath, issues, warnings
    
    except Exception as e:
        return filepath, [f"Error checking file: {str(e)}"], []

def find_all_html_files():
    """Find all HTML files in the website directory."""
    html_files = []
    website_dir = os.path.join(os.getcwd(), "website")
    
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    return html_files

def main():
    args = parse_args()
    
    start_time = time.time()
    
    print("Finding all HTML files...")
    html_files = find_all_html_files()
    print(f"Found {len(html_files)} HTML files.")
    
    # Check each HTML file
    results = []
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        
        for filepath in html_files:
            futures.append(executor.submit(check_html_file, filepath, args.check_links, args.verbose))
        
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error: {str(e)}")
    
    # Summarize results
    no_issues_files = []
    warnings_only_files = []
    issues_files = []
    
    issue_types = {}
    warning_types = {}
    
    for filepath, issues, warnings in results:
        if issues:
            issues_files.append((filepath, issues, warnings))
            for issue in issues:
                issue_type = issue.split(":")[0] if ":" in issue else issue
                if issue_type not in issue_types:
                    issue_types[issue_type] = []
                issue_types[issue_type].append(filepath)
        elif warnings:
            warnings_only_files.append((filepath, warnings))
            for warning in warnings:
                warning_type = warning.split(":")[0] if ":" in warning else warning
                if warning_type not in warning_types:
                    warning_types[warning_type] = []
                warning_types[warning_type].append(filepath)
        else:
            no_issues_files.append(filepath)
    
    print("\nVerification summary:")
    print(f"- Total files checked: {len(results)}")
    print(f"- Files with no issues: {len(no_issues_files)}")
    print(f"- Files with warnings only: {len(warnings_only_files)}")
    print(f"- Files with issues: {len(issues_files)}")
    print(f"- Time taken: {time.time() - start_time:.2f} seconds")
    
    # Print files with issues
    if issues_files:
        print("\nFiles with issues:")
        for filepath, issues, warnings in issues_files:
            rel_path = os.path.relpath(filepath, os.getcwd())
            print(f"- {rel_path}")
            for issue in issues:
                print(f"  - {issue}")
    
    # Group issues by type
    print("\nIssues by type:")
    for issue_type, filepaths in issue_types.items():
        print(f"- {issue_type}: {len(filepaths)} occurrences")
    
    # Group warnings by type
    print("\nWarnings by type:")
    for warning_type, filepaths in warning_types.items():
        print(f"- {warning_type}: {len(filepaths)} occurrences")
    
    # Write verification report
    with open("verification_report.txt", "w", encoding="utf-8") as f:
        f.write("Verification Report\n")
        f.write("==================\n\n")
        
        f.write("Summary:\n")
        f.write(f"- Total files checked: {len(results)}\n")
        f.write(f"- Files with no issues: {len(no_issues_files)}\n")
        f.write(f"- Files with warnings only: {len(warnings_only_files)}\n")
        f.write(f"- Files with issues: {len(issues_files)}\n")
        f.write(f"- Time taken: {time.time() - start_time:.2f} seconds\n\n")
        
        f.write("Files with issues:\n")
        for filepath, issues, warnings in issues_files:
            rel_path = os.path.relpath(filepath, os.getcwd())
            f.write(f"- {rel_path}\n")
            for issue in issues:
                f.write(f"  - {issue}\n")
        
        f.write("\nIssues by type:\n")
        for issue_type, filepaths in issue_types.items():
            f.write(f"- {issue_type}: {len(filepaths)} occurrences\n")
        
        f.write("\nWarnings by type:\n")
        for warning_type, filepaths in warning_types.items():
            f.write(f"- {warning_type}: {len(filepaths)} occurrences\n")
        
        f.write("\nDetailed list of files with issues:\n")
        for issue_type, filepaths in issue_types.items():
            f.write(f"\n{issue_type}:\n")
            for filepath in filepaths:
                rel_path = os.path.relpath(filepath, os.getcwd())
                f.write(f"- {rel_path}\n")
    
    print("\nVerification report written to verification_report.txt")

if __name__ == "__main__":
    main() 