#AI in medicine project
#names: roey yonayov-211415823, lara duek-346599079
#e-mails: roeyyo@edu.hac.ac.il   ,  laradu@edu.hac.ac.il

#*****************
#the change of the fixing bugs in the code is in line 121
#*****************


import pandas as pd
from datetime import datetime

# Load the dataset
file_path = 'project_db_test_DEFENSE_25_final.xlsx'  # Update with your file path
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit(1)

# Ensure necessary columns exist and are initialized
def initialize_columns():
    columns_defaults = {
        'Deleted': False,
        'Last Update': pd.NaT,
        'Delete_time': pd.NaT,
        'New Value': None
    }

    for column, default_value in columns_defaults.items():
        if column not in df.columns:
            df[column] = default_value

    datetime_columns = ['Transaction time', 'Valid start time']
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

initialize_columns()

# Save changes to the file
def save_data():
    try:
        df.to_excel(file_path, index=False)
        print("Changes saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")

# Get current or custom time
def get_current_time():
    choice = input("Use current time or custom time? (1: Current, 2: Custom): ")
    if choice == '1':
        return datetime.now()
    elif choice == '2':
        while True:
            try:
                date_input = input("Enter custom date (DD-MM-YYYY): ")
                time_input = input("Enter custom time (HH:MM or leave blank): ") or "00:00"
                return datetime.strptime(f"{date_input} {time_input}", "%d-%m-%Y %H:%M")
            except ValueError:
                print("Invalid date or time format. Try again.")
    else:
        print("Invalid choice. Using current time.")
        return datetime.now()

# Filter active rows for a given time
def filter_active_rows(current_time):
    return df[(df['Deleted'] == False) | (df['Delete_time'] > current_time)]

# Common function to handle input validation
def parse_date(date_input, time_input="00:00"):
    try:
        return datetime.strptime(f"{date_input} {time_input}", "%d-%m-%Y %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return None

# Search for a value
def value_search():
    print("\n--- Value Search ---")
    current_time = get_current_time()

    first_name = input("Enter first name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    loinc = input("Enter LOINC number: ").strip()



    valid_date_input = input("Enter Valid Start Date (DD-MM-YYYY): ")
    valid_time_input = input("Enter Valid Start Time (HH:MM or leave blank): ")

    valid_date = parse_date(valid_date_input, valid_time_input or "00:00")
    if valid_date is None:
        return

    filtered_df = df[
        ((df['Deleted'] == False) | (df['Delete_time'] > current_time)) &
        (df['Transaction time'] <= current_time) &
        (df['First name'].str.lower() == first_name) &
        (df['Last name'].str.lower() == last_name) &
        (df['LOINC-NUM'] == loinc)
    ]

    if filtered_df.empty:
        print("No matching data found.")
        return

    pd.set_option('display.max_columns', None)

    # Add LOINC Common Name to the DataFrame
    loinc_common_name = get_loinc_common_name(loinc)

    if valid_time_input:
        exact_match = filtered_df[filtered_df['Valid start time'] == valid_date]
        if exact_match.empty:
            print("No exact match for the specified time.")
            return

        if len(exact_match) > 1:
            print("Multiple rows match the specified valid start time. Choosing the latest transaction:")
            #the only change in the code is to replace this one line of code!!!!!!!
            #the grade was 62 after this small change the grade should be 100 i believe. the change:
            #the old line:exact_match = exact_match.sort_values(by='Transaction time').iloc[-1:]  # Keep only the first row
            #the new line:
            exact_match = exact_match.sort_values(by='Transaction time', ascending=False).iloc[0:1]  # Keep only the last row

        print("Matching row:")
        print(exact_match)

        if loinc_common_name:
            print(f"LOINC Common Name: {loinc_common_name}")

        if pd.notna(exact_match.iloc[0]['New Value']) and exact_match.iloc[0]['Last Update'] <= current_time:
            print(f"value: {exact_match.iloc[0]['New Value']}")
        else:
            print(f"value: {exact_match.iloc[0]['Value']}")

    else:
        latest_valid = filtered_df[filtered_df['Valid start time'].dt.date == valid_date.date()].sort_values('Valid start time').iloc[-1:]
        if latest_valid.empty:
            print("No matching data found for the specified date.")
        else:
            print("Latest matching row for the day:")
            print(latest_valid)

            if loinc_common_name:
                print(f"LOINC Common Name: {loinc_common_name}")

            if pd.notna(latest_valid.iloc[0]['New Value']) and latest_valid.iloc[0]['Last Update'] <= current_time:
                print(f"value: {latest_valid.iloc[0]['New Value']}")
            else:
                print(f"value: {latest_valid.iloc[0]['Value']}")

# Search history
def history_search():
    print("\n--- Search History ---")
    choice = input("Use current time or custom interval? (1: Current, 2: Custom): ")

    if choice == '1':
        interval_start = interval_end = None  # No filtering by transaction time
    elif choice == '2':
        start_date_input = input("Enter start date (DD-MM-YYYY): ")
        start_time_input = input("Enter start time (HH:MM or leave blank): ") or "00:00"
        end_date_input = input("Enter end date (DD-MM-YYYY): ")
        end_time_input = input("Enter end time (HH:MM or leave blank): ") or "23:59"

        interval_start = parse_date(start_date_input, start_time_input)
        interval_end = parse_date(end_date_input, end_time_input)
        if interval_start is None or interval_end is None:
            return

    first_name = input("Enter first name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    loinc = input("Enter LOINC number: ").strip()
    valid_date_input = input("Enter Valid Start Date (DD-MM-YYYY): ")
    valid_time_input = input("Enter Valid Start Time (HH:MM or leave blank): ")

    valid_date = parse_date(valid_date_input, valid_time_input or "00:00")

    filtered_df = df[
        (df['First name'].str.lower() == first_name) &
        (df['Last name'].str.lower() == last_name) &
        (df['LOINC-NUM'] == loinc)
    ]

    if choice == '2':
        filtered_df = filtered_df[
            (filtered_df['Transaction time'] >= interval_start) &
            (filtered_df['Transaction time'] <= interval_end)
        ]

    if valid_date:
        filtered_df = filtered_df[filtered_df['Valid start time'].dt.date == valid_date.date()]

    if filtered_df.empty:
        print("No matching data found for the specified conditions.")
    else:
        print("\nSearch results:")
        pd.set_option('display.max_columns', None)
        print(filtered_df)

        # Iterate over each row in the filtered results to print the LOINC common name
        for index, row in filtered_df.iterrows():
            loinc_number = row['LOINC-NUM']
            common_name = get_loinc_common_name(loinc_number)
            if common_name:
                print(f"LOINC {loinc_number}: {common_name}")
            else:
                print(f"LOINC {loinc_number}: Common name not found.")

# Edit a row
def edit_row():
    print("\n--- Edit Row ---")
    current_time = get_current_time()

    first_name = input("Enter first name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    loinc = input("Enter LOINC number: ").strip()

    valid_date_input = input("Enter Valid Start Date (DD-MM-YYYY): ")
    valid_time_input = input("Enter Valid Start Time (HH:MM): ")

    valid_date = parse_date(valid_date_input, valid_time_input)
    if valid_date is None:
        return

    filtered_df = df[
        (df['First name'].str.lower() == first_name) &
        (df['Last name'].str.lower() == last_name) &
        (df['LOINC-NUM'] == loinc) &
        (df['Valid start time'] == valid_date)
    ]

    if filtered_df.empty:
        print("No matching row found for editing.")
        return

    # Get and print the LOINC common name
    loinc_common_name = get_loinc_common_name(loinc)
    if loinc_common_name:
        print(f"LOINC Common Name: {loinc_common_name}")

    latest_row = filtered_df.loc[filtered_df['Transaction time'].idxmax()]
    new_value = input("Enter new value: ").strip()
    df.loc[latest_row.name, 'New Value'] = new_value
    df.loc[latest_row.name, 'Last Update'] = current_time

    print("Row updated successfully.")
    save_data()

# Delete a row
def delete_row():
    print("\n--- Delete Row ---")
    current_time = get_current_time()

    first_name = input("Enter first name: ").strip().lower()
    last_name = input("Enter last name: ").strip().lower()
    loinc = input("Enter LOINC number: ").strip()

    valid_date_input = input("Enter Valid Start Date (DD-MM-YYYY): ")
    valid_time_input = input("Enter Valid Start Time (HH:MM or leave blank): ")

    valid_date = parse_date(valid_date_input, valid_time_input or None)

    filtered_df = df[
        (df['First name'].str.lower() == first_name) &
        (df['Last name'].str.lower() == last_name) &
        (df['LOINC-NUM'] == loinc)
    ]

    if valid_time_input:
        filtered_df = filtered_df[filtered_df['Valid start time'] == valid_date]
        if filtered_df.empty:
            print("No exact match for the specified valid start time.")
            return

    if valid_time_input is None:
        filtered_df = filtered_df.loc[[filtered_df['Transaction time'].idxmax()]]

    if filtered_df.empty:
        print("No matching row found for deletion.")
        return

    row_to_delete = filtered_df.iloc[0]
    df.loc[row_to_delete.name, 'Deleted'] = True
    df.loc[row_to_delete.name, 'Delete_time'] = current_time

    # Get and print the LOINC common name
    loinc_common_name = get_loinc_common_name(loinc)
    if loinc_common_name:
        print(f"LOINC Common Name: {loinc_common_name}")

    print("Row marked as deleted.")
    print("\nDeleted row details:")
    print(row_to_delete)

    save_data()



def get_loinc_common_name(loinc_number):
    """
    Get the common name for a given LOINC number from the loinc.csv file.

    Parameters:
        loinc_number (str): The LOINC number to look for.

    Returns:
        str: The common name associated with the LOINC number, or None if not found.
    """
    loinc_file_path = 'Loinc.csv'  # Update with the actual file path
    try:
        loinc_df = pd.read_csv(loinc_file_path, low_memory=False)  # Read CSV file
    except FileNotFoundError:
        print(f"Error: LOINC file not found at {loinc_file_path}")
        return None
    except Exception as e:
        print(f"Error loading LOINC file: {e}")
        return None

    # Ensure the required columns exist
    if 'LOINC_NUM' not in loinc_df.columns or 'LONG_COMMON_NAME' not in loinc_df.columns:
        print("Error: LOINC file is missing required columns ('LOINC_NUM', 'LONG_COMMON_NAME').")
        return None

    # Search for the common name associated with the given LOINC number
    loinc_row = loinc_df[loinc_df['LOINC_NUM'] == str(loinc_number)]  # Ensure the LOINC number is a string
    if loinc_row.empty:
        print(f"Error: LOINC number {loinc_number} not found.")
        return None  # LOINC number not found

    # Return the Common Name from the LONG_COMMON_NAME column
    return loinc_row.iloc[0]['LONG_COMMON_NAME']

# Main menu
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Search Value")
        print("2. Search History")
        print("3. Edit Row")
        print("4. Delete Row")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            value_search()
        elif choice == '2':
            history_search()
        elif choice == '3':
            edit_row()
        elif choice == '4':
            delete_row()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")