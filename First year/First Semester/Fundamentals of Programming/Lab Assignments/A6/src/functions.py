#
# The program's functions are implemented here. There is no user interaction in this file, therefore no input/print statements. Functions here
# communicate via function parameters, the return statement and raising of exceptions. 
#
import random
import math


def create_complex_number(real_part, imaginary_part):
    return [real_part, imaginary_part]


def get_real_part(complex_number):
    return complex_number[0]


def get_imaginary_part(complex_number):
    return complex_number[1]


def get_operation_type(operation_stack):
    return operation_stack[0]


def get_operation_data(operation_stack):
    return operation_stack[1]


def set_real_part(complex_number, new_value):
    complex_number[0] = new_value


def set_imaginary_part(complex_number, new_value):
    complex_number[1] = new_value


def add_complex_number(real_part, imaginary_part, list_of_complex_numbers):
    """
    Adds a new complex number to the list of complex numbers
    """
    complex_number = create_complex_number(real_part, imaginary_part)
    list_of_complex_numbers.append(complex_number)

    return list_of_complex_numbers


def insert_complex_number(real_part, imaginary_part, position, list_of_complex_numbers):
    """
    Inserts a new complex number at a given position in the list of complex numbers
    """
    list_of_complex_numbers.insert(position, create_complex_number(real_part, imaginary_part))

    return list_of_complex_numbers


def remove_number_from_position(position, list_of_complex_numbers):
    """
    Removes a complex number from a given position in the list of complex numbers
    """
    try:
        del list_of_complex_numbers[position]
    except IndexError:
        print("Index out of bounds. Unable to delete.")

    return list_of_complex_numbers


def remove_number_from_interval(start_position, end_position, list_of_complex_numbers):
    """
    Removes all complex numbers from a given interval in the list of complex numbers
    """
    del list_of_complex_numbers[start_position:end_position + 1]

    return list_of_complex_numbers


def replace_number_from_position(real_part, imaginary_part, position, list_of_complex_numbers):
    """
    Replaces a complex number from a given position in the list of complex numbers
    """
    list_of_complex_numbers[position] = create_complex_number(real_part, imaginary_part)

    return list_of_complex_numbers


def display_list_of_complex_numbers(list_of_complex_numbers):
    """
    Displays the list of complex numbers
    """
    for i in range(len(list_of_complex_numbers)):
        print(f"{list_of_complex_numbers[i][0]} + {list_of_complex_numbers[i][1]}i")


def display_real_part_of_numbers_from_interval(start_position, end_position, list_of_complex_numbers):
    """
    Displays the real part of all complex numbers from a given interval in the list of complex numbers
    """
    for i in range(start_position, end_position):
        print(f"{list_of_complex_numbers[i][0]}")


def display_numbers_with_modulo_less_than_value(list_of_complex_numbers, modulo_value):
    """
    Displays all complex numbers with the modulo less than 10
    """
    for i in range(len(list_of_complex_numbers)):
        if math.sqrt(list_of_complex_numbers[i][0] ** 2 + list_of_complex_numbers[i][1] ** 2) < modulo_value:
            print(f"{list_of_complex_numbers[i][0]} + {list_of_complex_numbers[i][1]}i")


def display_numbers_with_modulo_greater_than_value(list_of_complex_numbers, modulo_value):
    """
    Displays all complex numbers with the modulo greater than 10
    """
    for i in range(len(list_of_complex_numbers)):
        if math.sqrt(list_of_complex_numbers[i][0] ** 2 + list_of_complex_numbers[i][1] ** 2) > modulo_value:
            print(f"{list_of_complex_numbers[i][0]} + {list_of_complex_numbers[i][1]}i")


def display_numbers_with_modulo_equal_to_value(list_of_complex_numbers, modulo_value):
    """
    Displays all complex numbers with the modulo equal to 10
    """
    for i in range(len(list_of_complex_numbers)):
        if math.sqrt(list_of_complex_numbers[i][0] ** 2 + list_of_complex_numbers[i][1] ** 2) == modulo_value:
            print(f"{list_of_complex_numbers[i][0]} + {list_of_complex_numbers[i][1]}i")


def filter_list_of_complex_numbers_by_real_part(list_of_complex_numbers):
    """
    Removes all complex numbers with the imaginary part equal to 0
    """
    len_of_list = len(list_of_complex_numbers)
    while len_of_list > 0:
        if list_of_complex_numbers[0][1] != 0:
            list_of_complex_numbers = remove_number_from_position(0, list_of_complex_numbers)
        len_of_list -= 1

    return list_of_complex_numbers


def filter_list_of_complex_numbers_by_modulo_less_than_value(list_of_complex_numbers, modulo_value):
    """
    Removes all complex numbers with the modulo less than 10
    """
    len_of_list = len(list_of_complex_numbers)
    while len_of_list > 0:
        if not math.sqrt(list_of_complex_numbers[0][0] ** 2 + list_of_complex_numbers[0][1] ** 2) < modulo_value:
            remove_number_from_position(0, list_of_complex_numbers)
        len_of_list -= 1

    return list_of_complex_numbers


def filter_list_of_complex_numbers_by_modulo_greater_than_value(list_of_complex_numbers, modulo_value):
    """
    Removes all complex numbers with the modulo greater than 10
    """
    len_of_list = len(list_of_complex_numbers)
    while len_of_list > 0:
        if not math.sqrt(list_of_complex_numbers[0][0] ** 2 + list_of_complex_numbers[0][1] ** 2) > modulo_value:
            remove_number_from_position(0, list_of_complex_numbers)
        len_of_list -= 1

    return list_of_complex_numbers


def filter_list_of_complex_numbers_by_modulo_equal_to_value(list_of_complex_numbers, modulo_value):
    """
    Removes all complex numbers with the modulo equal to 10
    """
    len_of_list = len(list_of_complex_numbers)
    while len_of_list > 0:
        if not math.sqrt(list_of_complex_numbers[0][0] ** 2 + list_of_complex_numbers[0][1] ** 2) == modulo_value:
            remove_number_from_position(0, list_of_complex_numbers)
        len_of_list -= 1

    return list_of_complex_numbers


def compute_undo_operation(list_of_complex_numbers, operation_stack):
    if not operation_stack:
        print("No operations to undo.")
        return list_of_complex_numbers

    last_operation = operation_stack.pop()
    operation_type, operation_data = last_operation

    if operation_type == "add":
        list_of_complex_numbers.pop()
    elif operation_type == "insert":
        index_to_remove = operation_data
        list_of_complex_numbers.pop(index_to_remove)
    elif operation_type == "remove":
        insert_complex_number(operation_data[0][0], operation_data[0][1], operation_data[1], list_of_complex_numbers)
    elif operation_type == "remove_from":
        index = 0
        for i in range(operation_data[0], operation_data[1]):
            list_of_complex_numbers.insert(i, create_complex_number(operation_data[2][index][0], operation_data[2][index][1]))
            index += 1
    elif operation_type == "replace":
        replaced_number, index_to_replace = operation_data
        list_of_complex_numbers[index_to_replace] = replaced_number
    elif operation_type == "filter_real_part":
        list_of_complex_numbers.clear()
        for i in range(len(operation_data)):
            list_of_complex_numbers.append(operation_data[i])
    elif operation_type == "filter_modulo":
        list_of_complex_numbers.clear()
        for i in range(len(operation_data)):
            list_of_complex_numbers.append(operation_data[i])

    return list_of_complex_numbers


def add_random_values_at_start():
    """
    Adds 10 random complex numbers to the list of complex numbers at program startup
    :return:
    """
    list_of_complex_numbers = []
    for i in range(10):
        list_of_complex_numbers.append(create_complex_number(random.randint(0, 100), random.randint(0, 100)))

    return list_of_complex_numbers
