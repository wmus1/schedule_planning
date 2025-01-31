import pandas as pd

# File path
file_path = r'C:\Users\DELL\Documents\scheduling_project1\ALCG Staff Contracted Hours Updated.xlsx'

# Load the Excel file without skipping any rows
df = pd.read_excel(file_path, header=None)  # header=None ensures no rows are treated as headers

# Print the raw DataFrame to inspect the structure
print("Raw DataFrame:")
print(df)

# Identify the columns for each set of data
# Assuming the first set of columns starts at column 0 and includes Middle Name
# Adjust these indices based on your actual file structure
first_set_columns = df.iloc[2:, 0:8]  # Columns 0, 1, 2, 3 (First Name, Middle Name, Surname, Hours)
second_set_columns = df.iloc[2:, 8:16]  # Columns 4, 5, 6, 7 (First Name, Middle Name, Surname, Hours)

# Rename the columns for consistency
first_set_columns.columns = ['First Name', 'Middle Name', 'Surname', 'Visa Status','Hours','31 Days','30 Days', '27 Days']
second_set_columns.columns = ['First Name', 'Middle Name', 'Surname', 'Visa Status','Hours','31 Days','30 Days', '27 Days']

# Combine both sets of data into a single DataFrame
combined_df = pd.concat([first_set_columns, second_set_columns], ignore_index=True)

# Drop rows with missing data (if any)
combined_df.dropna(subset=['First Name', 'Surname', 'Hours'], inplace=True)

# Print the combined DataFrame
print("\nCombined DataFrame:")
print(combined_df)

# Combine First Name, Middle Name, and Surname to create Full Name
combined_df['Full Name'] = combined_df['First Name'] + ' ' + combined_df['Middle Name'].fillna('') + ' ' + combined_df['Surname']

# Drop duplicate names and keep the first occurrence
unique_employees = combined_df.drop_duplicates(subset=['Full Name'])

# Extract the 'Full Name' and 'Hours' columns
employee_names = unique_employees['Full Name'].tolist()
employee_hours = unique_employees['Hours'].tolist()

# Combine names and hours into a list of tuples
employee_data = list(zip(employee_names, employee_hours))

# Print the results
print("\nEmployee Data:")
for name, hours in employee_data:
    print(f"Employee: {name}, Hours: {hours}")

# Optionally, save the unique data to a new Excel file
output_file_path = 'unique_employees.xlsx'
unique_employees.to_excel(output_file_path, index=False)
print(f"\nUnique employee data saved to {output_file_path}")