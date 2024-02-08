import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('live_love_yoga')

def get_arrived_data():
    """
    Getting arrived figures from the user from the last yoga classes
    """
    while True:
        print("Please enter arrived data from the last yoga class")
        print("Data should be six numbers, separated by commas.")
        print("Example: 1,2,3,4,5,6\n")
    
        data_str = input("Enter your data here: ")

        arrived_data = data_str.split(",")

        if validate_data(arrived_data):
            print("Data Approved")
            break

    return arrived_data


def validate_data(values):
    """
    We're validating 
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Receives a list of intergers to be inserted into a worksheet
    Updates the relevant worksheet with data provided
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet successfully updated.\n")


def calculate_surplus_data(arrived_row):
    """
    Calculating surplus data

    The surplus is defined by the arrived figure subtracted from expected figure
    - Positive surplus indicates the no shows (but reserved a mat space)
    - Negative surplus indicates the 
    """

    print("Calculating surplus data...\n")
    expected = SHEET.worksheet("expected").get_all_values()
    expected_row = expected[-1]

    surplus_data = []
    for expected, arrived in zip(expected_row,arrived_row):
        surplus = int(expected) - arrived
        surplus_data.append(surplus)
  
    return surplus_data

def get_arrived_entries():
    """

    Collects columns of data from worksheet
    """
    arrived = SHEET.worksheet("arrived") 
    columns = []
    for ind in range(1, 7):
        column = arrived.col_values(ind)
        columns.append(column[-5:])
        
    return columns


def calculate_expected_data(data):
    """
    calculate the average spaces 
    """

    print("Calculating expected data...\n")
    new_expected_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        expected_num = average * 1.1
        new_expected_data.append(round(expected_num))

    
    return new_expected_data
     


def main():
    """
    Runs all functions
    """
    data = get_arrived_data()
    arrived_data = [int(num) for num in data]
    update_worksheet(arrived_data, "arrived")
    new_surplus_data = calculate_surplus_data(arrived_data)
    update_worksheet(new_surplus_data, "surplus")
    arrived_columns = get_arrived_entries()
    expected_data = calculate_expected_data(arrived_columns)
    update_worksheet(expected_data, "expected")
    print(expected_data)

print("Welcome to Living Yoga Data Automation")
main()
