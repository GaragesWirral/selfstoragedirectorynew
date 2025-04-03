import pandas as pd

# Read the Excel file
df = pd.read_excel('self storage facilities uk.xlsx')

# Print column names
print("Columns:")
print(df.columns.tolist())

# Print first few rows
print("\nFirst 5 rows:")
print(df.head())

# Print some stats
print("\nTotal records:", len(df))
print("Unique regions:", df['Region'].nunique())
print("Unique cities:", df['CITY'].nunique())

# Print a few regions as example
print("\nSample regions:")
print(df['Region'].unique()[:10])

# Print a few cities as example
print("\nSample cities:")
print(df['CITY'].unique()[:10])

# Get count of storage facilities by region
print("\nNumber of storage facilities by region:")
region_counts = df['Region'].value_counts().sort_values(ascending=False)
print(region_counts.head(10)) 