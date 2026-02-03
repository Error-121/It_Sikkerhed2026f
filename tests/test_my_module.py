import pytest

def test_pass():
    # Denne test vil passere
    assert 1 + 1 == 2

def test_fail():
    # Denne test vil fejle
    assert 1 * 1 == 3


@pytest.mark.skip(reason="Springes over med vilje") # Denne test bliver slet ikke kørt
def test_skip():
    assert False # failed test bliver ignoreret
    raise RuntimeError("Test crashede med vilje") # crash bliver også ignoreret

def test_crash():
    # Denne test crasher med en exception
    raise RuntimeError("Test crashede med vilje")

    assert False # failed test bliver ignoreret

@pytest.mark.parametrize("x, y,expected", [
    (1, 2, 3), # Denne vil passere
    (2, 3, 4), # Denne vil fejle
    (3, 5, 8), # Denne vil passere
])

def test_parametrized_addition(x, y, expected):
    # Denne test kører flere gange med forskellige parametre
    assert x + y == expected

def test_crash_list_index():
    # Denne test crasher ved at tilgå et ugyldigt indeks i en liste
    lst = [1, 2, 3]
    _ = lst[5]  # Dette vil forårsage en IndexError

def test_string_concatenation():
    assert "hello".upper() + " world".upper() == "HELLO WORLD" # Denne test vil passere

def test_string_failure():
    assert "hello" + " world" == "HELLO WORLD" # Denne test vil fejle

def test_zero_division():
    # Denne test crasher ved division med nul
    _ = 1 / 0  # Dette vil forårsage en ZeroDivisionError

def test_list_membership():
    lst = [1, 2, 3, 4, 5]
    assert 3 in lst  # Denne test vil passere
    assert 6 in lst  # Denne test vil fejle

def test_dictionary_access():
    d = {'a': 1, 'b': 2}
    assert d['a'] == 1  # Denne test vil passere
    assert d['b'] == 2  # Denne test vil passere
    assert d['c'] == 3  # Denne test vil crashe med KeyError

