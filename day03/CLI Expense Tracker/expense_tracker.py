import csv
import os

FILE_NAME ="expenses.csv"
HEADER = ["id", "title", "amount", "category"]

def init_file():
    try:
        if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(HEADER)
    except Exception as e:
        print(f"Error initializing file: {e}")
        log_error(e)

# Read all expenses
def read_expenses():
    try:
        expenses = []

        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # skip rows without an amount as it will not consider as an expense
                if not row.get("amount"):
                    continue
                row["amount"] = float(row["amount"])
                expenses.append(row)
        return expenses

    except Exception as e:
        print(f"Error reading file: {e}")
        log_error(e)
        return []


# Add expense
def add_expense():
    try:
        title = input("Title: ")
        amount = float(input("Amount: "))
        category = input("Category: ")

        expenses = read_expenses()
        new_id = str(len(expenses) + 1)

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_id, title, amount, category])

        print("Expense added successfully!")
    except Exception as e:
        print(f"Error adding expense: {e}")
        log_error(e)



# Delete expense by id
def delete_expense():
    try:
        id_to_delete = input("Enter ID to delete: ")

        expenses = read_expenses()
        updated = [exp for exp in expenses if exp["id"] != id_to_delete]

        if len(updated) == len(expenses):
            print("No matching ID found!")
            return

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            for exp in updated:
                writer.writerow([exp["id"], exp["title"], exp["amount"], exp["category"]])

        print("Expense deleted!")

    except Exception as e:
        print(f"Error deleting expense: {e}")
        log_error(e)


# Update expense
def update_expense():
    try:
        id_to_update = input("Enter ID to update: ")

        expenses = read_expenses()
        found = False

        for exp in expenses:
            if exp["id"] == id_to_update:
                found = True
                print("Leave blank to keep old value.")
                new_title = input(f"Title ({exp['title']}): ")
                new_amount = input(f"Amount ({exp['amount']}): ")
                new_category = input(f"Category ({exp['category']}): ")

                exp["title"] = new_title
                exp["amount"] = float(new_amount)
                exp["category"] = new_category

        if not found:
            print("ID not found!")
            return

        # Save updated list
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            for exp in expenses:
                writer.writerow([exp["id"], exp["title"], exp["amount"], exp["category"]])
        print("Expense updated!")

    except Exception as e:
        print(f"Error updating expense: {e}")
        log_error(e)


# Show all expenses
def show_expenses():
    try:
        expenses = read_expenses()
        if not expenses:
            print("No expenses recorded.")
            return
        print("All Expenses:")
        for exp in expenses:
            print(f"{exp['id']}. {exp['title']} - {exp['amount']} ({exp['category']})")
    except Exception as e:
        print(f"Error showing expenses: {e}")
        log_error(e)


# logg errors to the file
def log_error(error):
    with open("errors.log", "a") as f:
        f.write(str(error) + "\n")

# Menu loop
def menu():
    try:
        init_file()
        while True:
            print("Expense Tracker")
            print("1. Add Expense")
            print("2. Delete Expense")
            print("3. Update Expense")
            print("4. View All Expenses")
            print("5. Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                add_expense()
            elif choice == "2":
                delete_expense()
            elif choice == "3":
                update_expense()
            elif choice == "4":
                show_expenses()
            elif choice == "5":
                break
            else:
                print("Invalid choice! Try again.")
    except Exception as e:
        print(f"Error in menu: {e}")
        log_error(e)

if __name__ == "__main__":
    menu()