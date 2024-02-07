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

def update_arrived_worksheet(data):
    """
    Update arrived worksheet
    """
    print("updating arrived worksheet...\n")
    arrived_worksheet = SHEET.worksheet("arrived")
    arrived_worksheet.append_row(data)
    print("Arrived worksheet successfully updated.\n")


data = get_arrived_data()
arrived_data = [int(num) for num in data]
update_arrived_worksheet(arrived_data)
