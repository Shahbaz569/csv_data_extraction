This Python script processes a CSV file, extracts specific rows that contain more than 70% non-null values, and analyzes package type keywords. It also handles data cleaning, such as removing "£" symbols from numeric values and ensures unique column names by appending suffixes to duplicates.

The script can be used for processing and extracting meaningful data from large CSV files.

**Requirements**

Python 3.x
pandas library
warnings library (standard in Python)
Install pandas
To install the pandas library, you can use pip:
pip install pandas
Functionality
extract_tables_from_csv(file_path)
This function processes a CSV file located at file_path. It performs the following tasks:

**Load CSV: Reads the CSV into a pandas DataFrame.**

Extract Rows with > 70% Non-Null Values: Filters rows where the percentage of non-null values is greater than 70%.
Set Headers: Sets the first row of the extracted rows as the header and renames columns.
Handle Duplicated Column Names: Ensures unique column names by appending a suffix to duplicate column names.
Package Type Identification: Searches for specific keywords (such as 'CTNS', 'QTN', 'Bags', etc.) in the rows and adds a "Package Type" column.
Data Cleaning: Strips the "£" symbol from numeric values.
The function returns:

rows_to_extract: A DataFrame containing the rows that meet the criteria.
remaining_rows: A DataFrame containing the rows that do not meet the criteria.
Example Usage
python
Copy code
import pandas as pd
from your_script_name import extract_tables_from_csv

**replace the file path**

file_path = '/path/to/your/file.csv'

**call the function**

extracted_rows, remaining_rows = extract_tables_from_csv(file_path)

**print the result**

print(extracted_rows)  # Rows with > 70% non-null values
print(remaining_rows)  # Rows with <= 70% non-null values
Function Parameters
file_path (str): The path to the CSV file you want to process.
Output
rows_to_extract: A DataFrame containing the extracted rows that have more than 70% non-null values. These rows are cleaned and have package type keywords identified.
remaining_rows: A DataFrame containing rows that do not meet the >70% non-null value criteria.GEM Imports Data Processing Script 
remaining_rows ia used for header Level information
This script processes a CSV file containing import data and extracts key information such as consignor details, consignee details, VAT numbers, package types, and total amounts. The extracted data is formatted into JSON for easy storage and access.

**Features**
Extracts consignor and consignee details including names, addresses, EORI numbers, and VAT numbers.
Identifies package types from the CSV data.
Processes gross weight and pallet details.
Extracts invoice numbers and total amounts.
Converts the extracted data into JSON format for easy integration into other systems.
Usage

**Setup:**


Ensure you have Python installed on your system.
Install the required Python packages (pandas and re).
Script Requirements:

A CSV file with the required format (must include fields like "Invoice Number", "Consignor Name", "Consignee Name", etc.).
Run the Script:

Replace the file_path variable in the script with the path to your CSV file.
Execute the script in your Python environment.
The script processes the file and generates a JSON file named GEM IMPORTS LTD.json.
How to Extract Data
Consignor and Consignee Details:

Extracts names, addresses, EORI numbers, and VAT numbers.
Parses data based on keywords like "GEM EORI" and "CUTGLASS EORI".
Package Types:

Identifies and categorizes package types (e.g., "CTNS", "QTN", "Pellate").
Invoice Numbers and Total Amounts:

Extracts invoice numbers and their corresponding amounts from the data.

**Export to JSON:**


The script converts the extracted data into a structured JSON format for easy storage.

**Dependencies**

pandas (for data manipulation)
re (for regular expression matching)
