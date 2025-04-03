import pandas as pd

def check_excel_structure():
    """Check the structure of the Excel file"""
    excel_path = 'self storage facilities uk.xlsx'
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_path)
        
        # Print the shape
        print(f"Excel file has {df.shape[0]} rows and {df.shape[1]} columns")
        
        # Print column names
        print("Column names:")
        for i, column in enumerate(df.columns):
            print(f"  {i+1}. {column}")
        
        # Print first 5 rows as a sample
        print("\nFirst 5 rows:")
        print(df.head())
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    check_excel_structure() 