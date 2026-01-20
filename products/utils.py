import string
import random


def generate_sku():
    # start with letters and then numbers
    letters = string.ascii_uppercase
    numbers = string.digits
    return "".join(random.choices(letters, k=6)) + "".join(random.choices(numbers, k=8))

print(generate_sku())