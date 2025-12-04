import csv
import os

class ExpenseTracker:
    FILE_NAME = "expenses.csv"
    HEADER = ["id", "title", "amount", "category"]

    def __init__(self):
        """initialize to ensure file exist"""
        self.init_file()

    def init_file(self):
        """create the csv file with a header if it does not exist or empty."""
        try:
            if not os.path.exists(self.FILE_NAME) or os.path.getsize(self.FILE_NAME) == 0:
                with open(self.FILE_NAME, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.HEADER)
        except Exception as e:
            print(f"Error initializing file: {e}")
            self.log_error(e)

    def read_expenses(self):
        try:
            """read all expenses"""
            expenses = []

            with open(self.FILE_NAME, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row.get("amount"):
                        continue
                    row["amount"] = float(row["amount"])
                    expenses.append(row)

            return expenses

        except Exception as e:
            print(f"Error reading file: {e}")
            self.log_error(e)
            return []

    def add_expense(self):
        """add new expense"""
        try:
            title = input("Title: ")
            amount = float(input("Amount: "))
            category = input("Category: ")

            expenses = self.read_expenses()
            new_id = str(len(expenses) + 1)

            with open(self.FILE_NAME, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([new_id, title, amount, category])

            print("Expense added successfully!")
        except Exception as e:
            print(f"Error adding expense: {e}")
            self.log_error(e)

    def delete_expense(self):
        """delete expense by id"""
        try:
            id_to_delete = input("Enter ID to delete: ")

            expenses = self.read_expenses()
            updated = [exp for exp in expenses if exp["id"] != id_to_delete]

            if len(updated) == len(expenses):
                print("No matching ID found!")
                return

            with open(self.FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.HEADER)
                for exp in updated:
                    writer.writerow([exp["id"], exp["title"], exp["amount"], exp["category"]])

            print("Expense deleted!")

        except Exception as e:
            print(f"Error deleting expense: {e}")
            self.log_error(e)

    def update_expense(self):
        """update existing expense"""
        try:
            id_to_update = input("Enter ID to update: ")

            expenses = self.read_expenses()
            found = False

            for exp in expenses:
                if exp["id"] == id_to_update:
                    found = True
                    print("Leave blank to keep old value.")
                    new_title = input(f"Title ({exp['title']}): ") or exp["title"]
                    new_amount = input(f"Amount ({exp['amount']}): ") or exp["amount"]
                    new_category = input(f"Category ({exp['category']}): ") or exp["category"]

                    exp["title"] = new_title
                    exp["amount"] = float(new_amount)
                    exp["category"] = new_category

            if not found:
                print("ID not found!")
                return

            with open(self.FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.HEADER)
                for exp in expenses:
                    writer.writerow([exp["id"], exp["title"], exp["amount"], exp["category"]])

            print("Expense updated!")

        except Exception as e:
            print(f"Error updating expense: {e}")
            self.log_error(e)

    def show_expenses(self):
        """show all expenses"""
        try:
            expenses = self.read_expenses()
            if not expenses:
                print("No expenses recorded.")
                return
            
            print("All Expenses:")
            for exp in expenses:
                print(f"{exp['id']}. {exp['title']} - {exp['amount']} ({exp['category']})")

        except Exception as e:
            print(f"Error showing expenses: {e}")
            self.log_error(e)

    def log_error(self, error):
        """Write error messages to a log file."""
        with open("errors.log", "a") as f:
            f.write(str(error) + "\n")

    def menu(self):
        """main menu"""
        try:
            while True:
                print("\nExpense Tracker")
                print("1. Add Expense")
                print("2. Delete Expense")
                print("3. Update Expense")
                print("4. View All Expenses")
                print("5. Exit")

                choice = input("Choose an option: ")
                if choice == "1":
                    self.add_expense()
                elif choice == "2":
                    self.delete_expense()
                elif choice == "3":
                    self.update_expense()
                elif choice == "4":
                    self.show_expenses()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice! Try again.")
        except Exception as e:
            print(f"Error in menu: {e}")
            self.log_error(e)


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.menu()