from contact_book.manager import add_contact, list_contacts

def test_list_contacts(temp_json):
    add_contact("A", "1")
    add_contact("B", "2")

    contacts = list_contacts()

    assert len(contacts) == 2
    assert contacts[0]["name"] == "A"
    assert contacts[1]["name"] == "B"