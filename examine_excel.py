import pandas as pd

# Read the Excel file
file_path = "self storage facilities uk.xlsx"
print(f"Reading Excel file: {file_path}")

try:
    # Read the Excel file
    excel_data = pd.read_excel(file_path)
    
    # Clean up column names
    excel_data.columns = [col.strip() for col in excel_data.columns]
    
    # Print basic information
    print(f"\nTotal records: {len(excel_data)}")
    print(f"\nColumns in the dataset:")
    for col in excel_data.columns:
        print(f"- {col}")
    
    # Print a sample of the data
    print("\nSample data (first 5 rows):")
    print(excel_data.head(5).to_string())
    
    # Check for unique regions
    if 'Region' in excel_data.columns:
        print(f"\nNumber of unique regions: {excel_data['Region'].nunique()}")
        print(f"\nUnique regions:")
        for region in sorted(excel_data['Region'].unique()):
            if pd.notna(region):
                print(f"- {region}")
    
    # Count facilities per region
    if 'Region' in excel_data.columns:
        region_counts = excel_data.groupby('Region').size().sort_values(ascending=False)
        print("\nRegions by number of facilities:")
        for region, count in region_counts.items():
            if pd.notna(region):
                print(f"- {region}: {count} facilities")
    
    # Sample of city data for Bedfordshire
    print("\nSample data for Bedfordshire (first 10 rows):")
    bedfordshire_data = excel_data[excel_data['Region'] == 'Bedfordshire'].head(10)
    print(bedfordshire_data[['CITY', 'Name of Self Storage', 'Website', 'Telephone Number', 'Location']].to_string())
    
    # Get all cities for a region with facility counts
    if 'Region' in excel_data.columns and 'CITY' in excel_data.columns:
        print("\nCities in Bedfordshire with facility counts:")
        bedfordshire_cities = excel_data[excel_data['Region'] == 'Bedfordshire'].groupby('CITY').size().sort_values(ascending=False)
        for city, count in bedfordshire_cities.items():
            print(f"- {city}: {count} facilities")
        
        # Example of Bedford facilities
        print("\nExample facilities in Bedford:")
        bedford_facilities = excel_data[(excel_data['Region'] == 'Bedfordshire') & (excel_data['CITY'].str.contains('Bedford', na=False))]
        for idx, row in bedford_facilities.iterrows():
            print(f"- {row['Name of Self Storage']}: {row['Telephone Number']} | {row['Website']}")
    
except Exception as e:
    print(f"Error reading Excel file: {e}") 