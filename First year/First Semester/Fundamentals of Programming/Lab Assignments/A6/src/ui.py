#
# This is the program's UI module. The user interface and all interaction with the user (print and input statements) are found here
#
import functions


def compute_add_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 3:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        real_part = int(command[1])
        imaginary_part = int(command[2])
    except ValueError:
        print("The real part and imaginary part of a complex number must be integers. Please try again")
        return list_of_complex_numbers, operation_stack
    operation_stack.append(["add", [real_part, imaginary_part]])
    list_of_complex_numbers = functions.add_complex_number(real_part, imaginary_part, list_of_complex_numbers)
    print(">>The complex number has been added")

    return list_of_complex_numbers, operation_stack


def compute_insert_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 5:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        real_part = int(command[1])
        imaginary_part = int(command[2])
        position = int(command[4])
    except ValueError:
        print("The real part, imaginary part and position of a complex number must be integers. Please try again")
        return list_of_complex_numbers, operation_stack
    operation_stack.append(["insert", position])
    list_of_complex_numbers = functions.insert_complex_number(real_part, imaginary_part, position, list_of_complex_numbers)
    print(">>The complex number has been inserted")

    return list_of_complex_numbers, operation_stack


def compute_remove_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 2:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        position = int(command[1])
    except ValueError:
        print("The position of a complex number must be an integer. Please try again")
        return list_of_complex_numbers, operation_stack
    operation_stack.append(["remove", [list_of_complex_numbers[position], position]])
    list_of_complex_numbers = functions.remove_number_from_position(position, list_of_complex_numbers)
    print(">>The complex number has been removed")

    return list_of_complex_numbers, operation_stack


def compute_remove_from_interval_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 4:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        start_position = int(command[1])
        end_position = int(command[3])
    except ValueError:
        print("The start position and end position of a complex number must be integers. Please try again")
        return list_of_complex_numbers, operation_stack
    operation_stack.append(["remove_from", [start_position, end_position, list_of_complex_numbers[start_position:end_position]]])
    list_of_complex_numbers = functions.remove_number_from_interval(start_position, end_position, list_of_complex_numbers)
    print(">>The complex numbers have been removed")

    return list_of_complex_numbers, operation_stack


def compute_replace_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 5:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        real_part = int(command[1])
        imaginary_part = int(command[2])
        position = int(command[4])
    except ValueError:
        print("The real part, imaginary part and position of a complex number must be integers. Please try again")
        return list_of_complex_numbers, operation_stack
    operation_stack.append(["replace", [list_of_complex_numbers[position], position]])
    list_of_complex_numbers = functions.replace_number_from_position(real_part, imaginary_part, position, list_of_complex_numbers)
    print(">>The complex number has been replaced")

    return list_of_complex_numbers, operation_stack


def compute_display_list_real_part_command(command, list_of_complex_numbers):
    if len(command) != 4:
        print("This is an invalid command. Please try again")
        return
    try:
        start_position = int(command[1])
        end_position = int(command[3])
    except ValueError:
        print("The start position and end position of a complex number must be integers. Please try again")
        return
    functions.display_real_part_of_numbers_from_interval(start_position, end_position, list_of_complex_numbers)


def compute_display_list_modulo_command(command, list_of_complex_numbers):
    if len(command) != 3:
        print("This is an invalid command. Please try again")
        return
    try:
        sign = command[1]
        value = int(command[2])
        if sign != "<" and sign != "=" and sign != ">":
            raise ValueError
    except ValueError:
        print("The sign or value is invalid. Please try again")
        return

    if sign == "<":
        functions.display_numbers_with_modulo_less_than_value(list_of_complex_numbers, value)
    elif sign == "=":
        functions.display_numbers_with_modulo_equal_to_value(list_of_complex_numbers, value)
    elif sign == ">":
        functions.display_numbers_with_modulo_greater_than_value(list_of_complex_numbers, value)


def compute_filter_real_part_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 1:
        print("This is an invalid command. Please try again")
        return
    copy_of_original_list = list_of_complex_numbers.copy()
    list_of_complex_numbers = functions.filter_list_of_complex_numbers_by_real_part(list_of_complex_numbers)
    operation_stack.append(["filter_real_part", copy_of_original_list])
    print(">>The complex numbers have been filtered")

    return list_of_complex_numbers, operation_stack


def compute_filter_modulo_operation(command, list_of_complex_numbers, operation_stack):
    if len(command) != 3:
        print("This is an invalid command. Please try again")
        return list_of_complex_numbers, operation_stack
    try:
        sign = command[1]
        value = int(command[2])
        if sign != "<" and sign != "=" and sign != ">":
            raise ValueError
    except ValueError:
        print("The sign is invalid. Please try again")
        return list_of_complex_numbers, operation_stack

    copy_of_original_list = list_of_complex_numbers.copy()
    operation_stack.append(["filter_modulo", copy_of_original_list])
    if sign == "<":
        list_of_complex_numbers = functions.filter_list_of_complex_numbers_by_modulo_less_than_value(list_of_complex_numbers, value)
    elif sign == "=":
        list_of_complex_numbers = functions.filter_list_of_complex_numbers_by_modulo_equal_to_value(list_of_complex_numbers, value)
    elif sign == ">":
        list_of_complex_numbers = functions.filter_list_of_complex_numbers_by_modulo_greater_than_value(list_of_complex_numbers, value)

    return list_of_complex_numbers, operation_stack


def compute_commands(command, list_of_complex_numbers, operation_stack):
    commands = ["add", "insert", "remove", "remove_from", "replace", "list", "list_real",
                "list_modulo", "filter_real_part", "filter_modulo", "undo", "exit"]

    if command[0] not in commands:
        print("This is an invalid command. Please try again")
        return
    if command[0] == "add":
        list_of_complex_numbers, operation_stack = compute_add_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "insert":
        list_of_complex_numbers, operation_stack = compute_insert_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "remove":
        list_of_complex_numbers, operation_stack = compute_remove_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "remove_from":
        list_of_complex_numbers, operation_stack = compute_remove_from_interval_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "replace":
        list_of_complex_numbers, operation_stack = compute_replace_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "list":
        functions.display_list_of_complex_numbers(list_of_complex_numbers)
    elif command[0] == "list_real":
        compute_display_list_real_part_command(command, list_of_complex_numbers)
    elif command[0] == "list_modulo":
        compute_display_list_modulo_command(command, list_of_complex_numbers)
    elif command[0] == "filter_real_part":
        list_of_complex_numbers, operation_stack = compute_filter_real_part_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "filter_modulo":
        list_of_complex_numbers, operation_stack = compute_filter_modulo_operation(command, list_of_complex_numbers, operation_stack)
    elif command[0] == "undo":
        list_of_complex_numbers = functions.compute_undo_operation(list_of_complex_numbers, operation_stack)
    elif command[0] == "exit":
        print(">>The program has been closed")
        return

    return list_of_complex_numbers, operation_stack


def print_ui():
    list_of_complex_numbers = functions.add_random_values_at_start()
    operation_stack = [["", []]]
    while True:
        print(">>List of commands: \n",
              "A. Add a number: \n",
              "add <real_part> <imaginary_part>\n",
              "insert <real_part> <imaginary_part> at <position>\n",
              "B. Modify numbers: \n",
              "remove <position>\n",
              "remove_from <start_position> to <end_position>\n",
              "replace <real_part> <imaginary_part> at <position>\n",
              "C. Display numbers having different properties: \n",
              "list\n",
              "list_real <start_position> to <end_position>\n",
              "list_modulo | < | = | > | <value>\n",
              "D. Filter the list: \n",
              "filter_real_part\n",
              "filter_modulo | < | = | > | <value>\n",
              "E. Undo the last operation: \n",
              "undo\n",
              "F. Exit the program: \n",
              "exit\n")
        print(">>Enter a command: ")
        command = input().split()
        compute_commands(command, list_of_complex_numbers, operation_stack)
