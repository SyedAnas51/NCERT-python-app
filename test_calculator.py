import pytest
from calculator import is_number, casting, add, subtract, multiply, divide


def test_is_number_valid():
    assert is_number("123") is True
    assert is_number("0.123") is True
    assert is_number("-0.123") is True


def test_is_number_invalid():
    assert is_number("") is False
    assert is_number("abc") is False


def test_casting_int():
    assert casting("5") == 5
    assert isinstance(casting("5"), int)


def test_casting_float():
    assert casting("5.5") == 5.5
    assert isinstance(casting("5.5"), float)


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
