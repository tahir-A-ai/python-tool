import pytest # type: ignore
from contact_book.storage import DATA_FILE

@pytest.fixture
def temp_json(tmp_path, monkeypatch):
    temp_file = tmp_path / "contacts.json"
    temp_file.write_text("[]")

    # override the DATA_FILE path
    monkeypatch.setattr("contact_book.storage.DATA_FILE", str(temp_file))

    return temp_file