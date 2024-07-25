
from datetime import datetime

DATE_FORMAT= "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default= False):
    '''
    Function to get the date from the user and validate it
    '''
    date_str = input(prompt)
    
    
    #if user not entered date, insert today date
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)
    
    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("Invlid Date Format!, please enter date in dd-mm-yyyy format")
        get_date(prompt, allow_default)
    


def get_amount():
    '''
    Function to get the amount of Transaction
    '''
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount should be non-zero non-negative value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category =  input("Enter the Category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category, Please enter 'I'-Income or 'E'-Expense.")
    return get_category()




def get_description():
    return input("Enter a description (optional): ")
