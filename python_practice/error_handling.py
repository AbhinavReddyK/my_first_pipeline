# Error Handling Practice
# Learned: try, except, finally

try:
    x = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except ValueError:
    print("Wrong value!")
finally:
    print("Always runs!")
