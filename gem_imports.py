# -*- coding: utf-8 -*-
"""GEM IMPORTS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vIqaHeM6JNtmj6Hk0enksVh9ASPDES7W
"""



import pandas as pd
import re
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")
import pandas as pd

def extract_tables_from_csv(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Identify rows where the percentage of non-null values is greater than 70%
    non_null_counts = df.notna().sum(axis=1)
    total_columns = df.shape[1]
    non_null_percentage = (non_null_counts / total_columns) * 100
    rows_to_extract = df[non_null_percentage > 70]
    remaining_rows = df[non_null_percentage <= 70]  # Separate the remaining rows

    # Check if any rows were extracted
    if rows_to_extract.empty:
        print("No rows with more than 70% non-null values found.")
        return pd.DataFrame(), remaining_rows

    # Set the first row of the extracted rows as the header
    rows_to_extract.columns = rows_to_extract.iloc[0]  # Set the first row as header
    rows_to_extract = rows_to_extract[1:]  # Remove the first row from the data

    # Rename columns with NaN names
    rows_to_extract.columns = [
        f"Unnamed{i+1}" if pd.isna(col) else col
        for i, col in enumerate(rows_to_extract.columns)
    ]

    # Ensure unique column names by appending a suffix to duplicates
    columns = pd.Series(rows_to_extract.columns)
    for dup in columns[columns.duplicated()].unique():
        # Append a number to duplicate column names
        columns[columns[columns == dup].index.values.tolist()] = [
            f"{dup}_{i+1}" if i != 0 else dup
            for i in range(sum(columns == dup))
        ]
    rows_to_extract.columns = columns  # Update the DataFrame columns

    # Define possible package type keywords
    package_type_keywords = ['CTNS', 'QTN', 'Pellate', 'Boxes', 'Euro Pellate', 'Bags', 'Cases', 'Carton']

    # Check each row for package type keywords and populate "Package Type" column
    rows_to_extract['Package Type'] = rows_to_extract.apply(
        lambda row: next(
            (keyword for keyword in package_type_keywords if keyword in row.to_string()),
            None
        ),
        axis=1
    )

    # Clean up "£" symbols from numeric values
    rows_to_extract = rows_to_extract.applymap(
        lambda x: str(x).replace("£", "").strip() if isinstance(x, str) and "£" in x else x
    )

    return rows_to_extract, remaining_rows

# Replace with your actual file path
file_path = '/content/GEM IMPORTS LTD.csv'

# Call the function
extracted_rows, remaining_rows = extract_tables_from_csv(file_path)
data = remaining_rows
results = []

# Loop through the DataFrame rows (assuming 'data' is your DataFrame)
for index, row in data.iterrows():
    for col_index, cell in enumerate(row):
        if isinstance(cell, str) and "Invoice Number:" in cell:
            # Get the two right cells
            if col_index + 2 < len(row):
                # Extract the next two cells and filter out empty or NaN values
                result = [value for value in row[col_index + 1: col_index + 3] if pd.notna(value) and value != ""]
                if result:  # Only append if there are non-empty values
                    results.append(result)

# Assuming 'extracted_rows' is already created with other columns
# Handle case where results' length might not match extracted_rows length
if len(results) > 0:
    reference_number = results[0][0]  # Take the first reference number from the results
    extracted_rows['Reference Number'] = [reference_number] * len(extracted_rows)
else:
    # If no reference numbers found, set as None or empty string
    extracted_rows['Reference Number'] = [None] * len(extracted_rows)

# Map 'Carton' to 'CTN' in the 'Package Type' column
extracted_rows['Package Type'] = extracted_rows['Package Type'].apply(
    lambda x: 'CTN' if x == 'Carton' else x
)



data =remaining_rows
print(f"Form Field: {''}")
# Extract Consigner Name and Street (with regex)
consigner_name_and_street = remaining_rows.applymap(lambda x: x if pd.notnull(x) and bool(pd.Series(x).str.contains(r'\bHoyland\b', regex=True).iloc[0]) else None)
consigner_name_and_street.dropna(how='all', inplace=True)

# Print Consigner Name and Street
for cell in consigner_name_and_street.values.flatten():
    if pd.notna(cell):
        parts = cell.split(',', 1)
        consigner_name = parts[0].strip()
        consignee_street_name = parts[1].strip() if len(parts) > 1 else "N/A"
        print(f"Consigner : {consigner_name}\nConsigner Street : {consignee_street_name}")
# Function to extract GEM EORI or CUTGLASS EORI
def extract_eori_value(text, eori_type):
    match = re.search(f'{eori_type} EORI\s+(\S+)', str(text))
    return match.group(1) if match else None

# Extract Consigner EORI
consigner_eori_values = remaining_rows.applymap(lambda x: extract_eori_value(x, 'GEM'))
consigner_eori_values.dropna(how='all', inplace=True)
consigner_eori_values.dropna(axis=1, how='all', inplace=True)

# Print Consigner EORI
for value in consigner_eori_values.values.flatten():
    if pd.notna(value):
        print(f"Consigner id: {value}")
# Extract VAT Number (Consigner VAT)
def extract_vat_number(text):
    match = re.search(r'Vat No:\s+(\d+(\s\d+)*)', str(text))
    return match.group(1).replace(" ", " ") if match else None

vat_values = remaining_rows.applymap(extract_vat_number)
vat_values.dropna(how='all', inplace=True)
vat_values.dropna(axis=1, how='all', inplace=True)

# Print VAT Number
for value in vat_values.values.flatten():
    if pd.notna(value):
        print(f"Consigner Vat: {value}")

        for i, row in data.iterrows():
            if 'Invoice To:' in str(row[0]):  # assuming 'Invoice To:' is in the first column (adjust if necessary)
                # Extract the next 4 rows (below 'Invoice To:')
                consignee_data = data.iloc[i+1:i+6, 0].tolist()  # Adjust the column index if needed

                # Assign values to respective fields
                consignee_name = consignee_data[0]  # Consignee name is in the first element
                consignee_street = " ".join(consignee_data[1:4])  # Join street address parts into one string
                consignee_country = consignee_data[4]  # Country is in the fifth element

                # Print the extracted information
                print(f"Consignee : {consignee_name}")
                print(f"Consignee Street: {consignee_street}")  # Now street address will print without brackets
                print(f"Consignee Country: {consignee_country}")

# Extract Consignee EORI
consignee_eori_values = remaining_rows.applymap(lambda x: extract_eori_value(x, 'CUTGLASS'))
consignee_eori_values.dropna(how='all', inplace=True)
consignee_eori_values.dropna(axis=1, how='all', inplace=True)

# Print Consignee EORI
for value in consignee_eori_values.values.flatten():
    if pd.notna(value):
        print(f"Consignee id: {value}")


# Extract Invoice Number
invoice_numbers = []
for index, row in remaining_rows.iterrows():
    for col_index, cell in enumerate(row):
        if isinstance(cell, str) and "Invoice Number:" in cell:
            if col_index + 2 < len(row):
                result = [value for value in row[col_index + 1: col_index + 3] if pd.notna(value) and value != ""]
                if result:
                    invoice_numbers.append(result)

# Print Invoice Numbers
for res in invoice_numbers:
    print(f"Reference no ucr: {res[0]}")
import pandas as pd
import re

# Function to extract all words after 'Origin' and map "China" to "CN"
def extract_and_map_text(text):
    # Search for variations of the keyword and extract everything after 'Origin'
    match = re.search(r'Origin\s+(\S+)(.*)', str(text))
    if match:
        extracted_text = match.group(2).strip()  # Extract everything after 'Origin'
        # Map "China" or similar values to "CN"
        if "China" in extracted_text:
            return "CN"
        return extracted_text
    return None  # Return None if no match is found

# Apply the function across all cells in the DataFrame
remaining_text_values = data.applymap(extract_and_map_text)

# Drop rows and columns that do not contain relevant data (optional)
remaining_text_values.dropna(how='all', inplace=True)
remaining_text_values.dropna(axis=1, how='all', inplace=True)

# Convert the DataFrame to a simple list of values and print without index and column names
remaining_text_values_flat = remaining_text_values.values.flatten()
for value in remaining_text_values_flat:
    if pd.notna(value):  # Only print non-null values
        print(f"H_Country_of_origin: {value}")


# Extract Gross Weight (Total Gross Mass)
def extract_gross_weight(text):
    match = re.search(r'Gross Weight\s+(\S+)', str(text))
    return match.group(1) if match else None

gross_weight_values = remaining_rows.applymap(extract_gross_weight)
gross_weight_values.dropna(how='all', inplace=True)
gross_weight_values.dropna(axis=1, how='all', inplace=True)

# Print Gross Weight
for value in gross_weight_values.values.flatten():
    if pd.notna(value):
        print(f"H-total gross mass: {value}")

# Extract Pallets (Total Package Quantity)
def extract_pallets(text):
    match = re.search(r'Pallets\s+(\S+)', str(text))
    return match.group(1) if match else None

pallets_values = remaining_rows.applymap(extract_pallets)
pallets_values.dropna(how='all', inplace=True)
pallets_values.dropna(axis=1, how='all', inplace=True)

# Print Pallets (Total Package Quantity)
for values in pallets_values.values.flatten():
    if pd.notna(values):
        print(f"H-total packages: {values}")

# Function to extract all words after 'Total Pallets 4' and map 'pallets' to 'PX'
def extract_remaining_text(text):
    # Search for the pattern "Total Pallets 4" and extract everything after it
    match = re.search(r'Total Pallets 4\s+(\S.*)', str(text))
    if match:
        extracted_text = match.group(1).strip()
        # Map 'pallets' to 'PX' in the extracted text
        mapped_text = re.sub(r'\bpallets\b', 'PX', extracted_text, flags=re.IGNORECASE)
        return mapped_text
    return None  # Return None if no match is found

# Apply the function across all cells in the DataFrame
remaining_text_values = data.applymap(extract_remaining_text)

# Drop rows and columns that do not contain relevant data (optional)
remaining_text_values.dropna(how='all', inplace=True)
remaining_text_values.dropna(axis=1, how='all', inplace=True)

# Convert the DataFrame to a simple list of values and print without index and column names
remaining_text_values_flat = remaining_text_values.values.flatten()
for value in remaining_text_values_flat:
    if pd.notna(value):  # Only print non-null values
        print(f"H_Packgae_type: {value}")
import pandas as pd

results = []

# Loop through the dataframe rows
for index, row in data.iterrows():
    for col_index, cell in enumerate(row):
        if isinstance(cell, str) and "Grand Total:" in cell:
            # Get all cells to the right of "Grand Total:"
            right_cells = row[col_index + 1:]
            # Find the last non-empty value
            last_value = right_cells.dropna().iloc[-1] if not right_cells.dropna().empty else None
            if last_value is not None:
                # Remove '£' if present and append the cleaned value
                results.append(str(last_value).replace("£", "").strip())

# Output the results
for res in results:
    print(f"H-Total Amount: {res}")
    print(f"Table Data: {''}")
    print(extracted_rows)

import json
import os

# Example: get the file name dynamically (replace this part with how you get the actual file name) # Replace with actual file path
file_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract file name without extension

# Initialize header JSON
header_json = []

# Example consignor and consignee details (replace with your actual extracted values)
consignor_details = {
    "Consignor Name": consigner_name,
    "Consignor Street": consignee_street_name,
    "Consignor EORI": next(iter(consigner_eori_values.values.flatten()), None),
    "Consignor VAT": next(iter(vat_values.values.flatten()), None),
}

consignee_details = {
    "Consignee Name": consignee_name,
    "Consignee Street": consignee_street,
    "Consignee Country": consignee_country,
    "Consignee EORI": next(iter(consignee_eori_values.values.flatten()), None),
}

# Add consignor details to JSON
for key, value in consignor_details.items():
    header_json.append({"key": {"key_text": key}, "value": {"value_text": value}})

# Add consignee details to JSON
for key, value in consignee_details.items():
    header_json.append({"key": {"key_text": key}, "value": {"value_text": value}})

# Example dynamic fields (replace with your actual extracted values)
dynamic_fields = [
    {"key_text": "Reference Number UCR / Invoice Number", "value_text": extracted_rows['Reference Number'].iloc[0] if not extracted_rows.empty else ''},
    {"key_text": "H-package type", "value_text": extracted_rows['Package Type'].iloc[0] if not extracted_rows.empty else ''},
    {"key_text": "H-Total Packages", "value_text": values},  # Replace with your actual value
    {"key_text": "H-Total Gross Mass", "value_text": next(iter(gross_weight_values.values.flatten()), None)},
    {"key_text": "H-Total Amount", "value_text": results[0] if results else ''},
]

# Add dynamic fields to JSON
for field in dynamic_fields:
    header_json.append({"key": {"key_text": field['key_text']}, "value": {"value_text": field['value_text']}})

# Prepare table_data (replace with actual logic to generate table data from DataFrame)
table_json = []

# Reset the index to start from 0 if necessary
extracted_rows.reset_index(drop=True, inplace=True)

# Add the header to the table JSON output
for col_index, column in enumerate(extracted_rows.columns):
    table_json.append({
        "row": 0,  # Row index for header is 0
        "column": col_index,
        "text": str(column)  # Column name as text
    })

# Iterate over each row and column in the DataFrame (data starts from row 1)
for row_index, row in extracted_rows.iterrows():
    for col_index, cell in enumerate(row):
        table_json.append({
            "row": row_index + 1,  # Data rows start from index 1
            "column": col_index,
            "text": str(cell)  # Cell content
        })

# Combine everything into the final JSON structure
final_json = {
    file_name: {  # Use the dynamic file name here
        "resulting_data": {
            "form_fields": header_json,  # Include all form fields
            "table_data": table_json     # Include table data
        }
    }
}

# Save the final JSON to a file
output_file_path = "GEM IMPORTS LTD.json"
with open(output_file_path, "w") as json_file:
    json.dump(final_json, json_file, indent=4)

print(f"JSON file saved as {output_file_path}")