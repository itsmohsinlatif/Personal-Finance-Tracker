import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt
plt.ion()  #Turn on Interactive mode



class CSVHandler:
    '''
    CSV file to store the entries data
    '''

    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        """
        Initialize the csv file, if not already there
        """

        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index= False)

            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        '''
        Method to add the entry of transaction
        '''
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        # writing entry into file
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added, successfully")


    @classmethod
    def get_transactions(cls, start_date, end_date):
        '''
        Function to get the transactions from DB against given dates
        '''
        df = pd.read_csv(cls.CSV_FILE)
        #Perform date formatting on date column
        df['date'] = pd.to_datetime(df["date"], format= CSVHandler.DATE_FORMAT)
        #Also convert given dates into same datetime format
        start_date = datetime.strptime(start_date, CSVHandler.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSVHandler.DATE_FORMAT)

        #Create mask to apply on dataframe
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        #Apply mask to get rows within range
        filtered_df = df.loc[mask]

        #printing the transactions
        if filtered_df.empty:
            print("No Transactions found in given date range!")
        else:
            print(f"Transactions from {start_date.strftime(CSVHandler.DATE_FORMAT)} to {end_date.strftime(CSVHandler.DATE_FORMAT)}")
            #print transaction rows by date format
            print(
                filtered_df.to_string(
                    index= False, formatters= {"date": lambda x: x.strftime(CSVHandler.DATE_FORMAT)}
                )
            )
            
            #income and expenses
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        
        return filtered_df
    

def plot_transactions(df, output_file= "transaction_plot.png"):
    '''
    Function to plot the transacations in line graph
    '''
    #need to do formatting on date column
    df.set_index("date", inplace= True)

    income_df = (
            df[df["category"] == "Income"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value= 0)  #to fill with dates with null transactions entries
                 )
    expense_df = (
            df[df["category"] == "Expense"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value= 0)  #to fill with dates with null transactions entries
                 )
    plt.figure(figsize= (10, 5))
    plt.plot(income_df.index, income_df["amount"], label= "Income", color= "g")
    plt.plot(expense_df.index, expense_df["amount"], label= "Expense", color= "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()




def add():
    CSVHandler.initialize_csv()
    date = get_date("Enter the transaction date (dd-mm-yyyy) or press Enter for today's date: ", allow_default= True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSVHandler.add_entry(date, amount, category, description)




def main():
    while True:
        print("\n1. Add new Transaction")
        print("2. View Transactions and summary within date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSVHandler.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df, output_file= "transaction_plot.png")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid Choice! Enter 1, 2 or 3")



if __name__ == "__main__":
    main()
