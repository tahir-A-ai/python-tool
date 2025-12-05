from contact_book.models import create_contact
from contact_book.storage import load_contacts, save_contacts


def add_contact(name, phone):
    contacts = load_contacts()
    try:
        contacts.append(create_contact(name, phone))
        save_contacts(contacts)
        return True
    except Exception:
        return False


def delete_contact(name):
    contacts = load_contacts()
    try:
        new_list = [c for c in contacts if c["name"] != name]
        save_contacts(new_list)
        return True
    except Exception:
        return False


def update_contact(name, new_phone):
    contacts = load_contacts()
    found = False

    try:
        for c in contacts:
            if c["name"] == name:
                c["phone"] = new_phone
                found = True

        save_contacts(contacts)
        return found
    except Exception:
        return False


def list_contacts():
    return load_contacts()