from contact_book.manager import (
    add_contact,
    delete_contact,
    update_contact,
    list_contacts,
)


def menu():
    while True:
        print("********* CONTACT BOOK *********")
        print("1. Add Contact")
        print("2. Delete Contact")
        print("3. Update Contact")
        print("4. List Contacts")
        print("5. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input.")
            continue

        if choice == 1:
            name = input("Name: ")
            phone = input("Phone: ")
            if add_contact(name, phone):
                print("Contact added.")
            else:
                print("Failed to add.")

        elif choice == 2:
            name = input("Name to delete: ")
            if delete_contact(name):
                print("Deleted.")
            else:
                print("Failed to delete.")

        elif choice == 3:
            name = input("Name to update: ")
            new_phone = input("New phone: ")
            if update_contact(name, new_phone):
                print("Updated.")
            else:
                print("Contact not found.")

        elif choice == 4:
            contacts = list_contacts()
            if not contacts:
                print("No contacts found.")
            else:
                for c in contacts:
                    print(f"{c['name']} – {c['phone']}")

        elif choice == 5:
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
