from contact_book.manager import add_contact, list_contacts

def test_add_contact(temp_json):
    add_contact("Ali", "0300000")
    contacts = list_contacts()

    assert len(contacts) == 1
    assert contacts[0]["name"] == "Ali"
    assert contacts[0]["phone"] == "0300000"