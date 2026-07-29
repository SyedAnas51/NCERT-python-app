"""
Core calculator logic, separated from the Tkinter GUI so it can be
unit tested in CI without a display.
"""


def is_number(s):
    if s == '':
        return False
    if s.replace('.', '', 1).isdigit():
        return True
    if s.isdigit():
        return True
    if s[0] in ['-', '+', '.', '0', ' ']:
        if len(s) > 1 and s[1] == '.':
            if s[2:].isdigit():
                return True
        if len(s) > 2 and s[1] == '0' and s[2] == '.':
            if s[3:].isdigit():
                return True
        if s[1:].isdigit():
            return True
    return False


def casting(num):
    if '.' in num:
        return float(num)
    return int(num)


def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    return num1 * num2


def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return num1 / num2
