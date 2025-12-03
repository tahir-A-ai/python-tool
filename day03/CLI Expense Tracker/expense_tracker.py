import csv
import os

FILE_NAME = "expenses.csv"

def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "title", "amount", "category"])


# Read all expenses
def read_expenses():
    try:
        expenses = []

        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)

        return expenses

    except Exception as e:
        print(f"Error reading file: {e}")
        return []


# Add expense
def add_expense():
    try:
        title = input("Title: ")
        amount = float(input("Amount: "))
        category = input("Category: ")

        expenses = read_expenses()
        new_id = len(expenses) + 1

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_id, title, amount, category])

        print("Expense added successfully!")

    except Exception as e:
        print(f"Error adding expense: {e}")


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
            writer.writerow(["id", "title", "amount", "category"])
            for exp in updated:
                writer.writerow(exp.values())

        print("Expense deleted!")

    except Exception as e:
        print(f"Error deleting expense: {e}")


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
                new_title = input(f"Title ({exp['title']}): ") or exp['title']
                new_amount = input(f"Amount ({exp['amount']}): ") or exp['amount']
                new_category = input(f"Category ({exp['category']}): ") or exp['category']

                exp["title"] = new_title
                exp["amount"] = float(new_amount)
                exp["category"] = new_category

        if not found:
            print("ID not found!")
            return

        # Save updated list
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "title", "amount", "category"])
            for exp in expenses:
                writer.writerow(exp.values())

        print("Expense updated!")

    except Exception as e:
        print(f"Error updating expense: {e}")


# Show all expenses
def show_expenses():
    expenses = read_expenses()

    if not expenses:
        print("No expenses recorded.")
        return

    print("\n---- All Expenses ----")
    for exp in expenses:
        print(f"{exp['id']}. {exp['title']} - {exp['amount']} ({exp['category']})")
    print("----------------------\n")


# Menu loop
def menu():
    init_file()

    while True:
        print("\nExpense Tracker")
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


if __name__ == "__main__":
    menu()