from contact_book.manager import add_contact, delete_contact, list_contacts

def test_delete_contact(temp_json):
    add_contact("Bob", "111")

    deleted = delete_contact("Bob")

    assert deleted is True
    assert list_contacts() == []