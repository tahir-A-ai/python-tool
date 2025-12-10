import pytest # type: ignore

""" Assertions"""
def test_add():
    assert 2+3 == 5

def test_subt():
    assert 10-4 == 6

def test_bool():
    assert 5>0

def test_membership():
    users = ['user1', 'admin']
    assert "admin" in users

def divided_by_zero(a, b):
    return a/b
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        divided_by_zero(4,0)


""" Fixtures >> provide reusable data, can be used in any test case later """
@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_sum(sample_list):
    assert sum(sample_list) == 6


"""
fixture also provide creating temp Dir for test cases,
once testing done, the Dir vanished!
"""
@pytest.fixture
def file(tmp_path):
    file = tmp_path/ "data.txt"
    file.write_text("10\n20\n30")
    return file

def test_file(file):
    content = file.read_text()
    assert "20" in content