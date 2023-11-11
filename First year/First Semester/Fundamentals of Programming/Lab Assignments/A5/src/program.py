#
# Write the implementation for A5 in this file
#

# 
# Write below this comment 
# Functions to deal with complex numbers -- list representation
# -> There should be no print or input statements in this section 
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#

import random


def create_complex_number(real_part, imaginary_part):
    return [real_part, imaginary_part]


def get_real_part(complex_number):
    return complex_number[0]


def get_imaginary_part(complex_number):
    return complex_number[1]


def get_real_part_list(complex_number_list):
    real_part_list = []
    for complex_number in complex_number_list:
        real_part_list.append(get_real_part(complex_number))

    return real_part_list


def set_real_part(complex_number, new_real_part):
    complex_number[0] = new_real_part


def set_imaginary_part(complex_number, new_imaginary_part):
    complex_number[1] = new_imaginary_part


def convert_complex_number_to_string(complex_number):
    return str(get_real_part(complex_number)) + " + " + str(get_imaginary_part(complex_number)) + "i"

#
# Write below this comment 
# Functions to deal with complex numbers -- dict representation
# -> There should be no print or input statements in this section 
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#

# def create_complex_number(real_part, imaginary_part):
#    return {"real": real_part, "imaginary": imaginary_part}


# def get_real_part(complex_number):
#    return complex_number["real"]


# def get_imaginary_part(complex_number):
#    return complex_number["imaginary"]


# def set_real_part(complex_number, new_real_part):
#    complex_number["real"] = new_real_part


# def set_imaginary_part(complex_number, new_imaginary_part):
#    complex_number["imaginary"] = new_imaginary_part

#
# Write below this comment 
# Functions that deal with subarray/subsequence properties
# -> There should be no print or input statements in this section 
# -> Each function should do one thing only
# -> Functions communicate using input parameters and their return values
#

def generate_complex_numbers_at_startup():
    complex_number_list = []
    for i in range(10):
        complex_number_list.append(create_complex_number(random.randint(1, 50), random.randint(1, 50)))

    return complex_number_list


def is_a_mountain_subset(subarray):
    length_of_subarray = len(subarray)

    # A mountain should have at least 3 elements
    if length_of_subarray < 3:
        return False

    # Find the peak of the mountain
    peak = max(subarray)
    peak_index = subarray.index(peak)

    # If the peak is the first or last element, it's not a mountain
    if peak_index == 0 or peak_index == length_of_subarray - 1:
        return False

    # Check if the first part is increasing
    for i in range(peak_index):
        if subarray[i] >= subarray[i + 1]:
            return False

    # Check if the second part is decreasing
    for i in range(peak_index, length_of_subarray - 1):
        if subarray[i] <= subarray[i + 1]:
            return False

    return True


def find_longest_subarray_where_the_real_part_is_a_mountain(real_part_list):
    longest_mountain_subarray = []
    length_of_longest_mountain_subarray = 0

    for i in range(len(real_part_list)):
        for j in range(i, len(real_part_list)):
            subarray = real_part_list[i:j + 1]
            if is_a_mountain_subset(subarray) and len(subarray) > length_of_longest_mountain_subarray:
                longest_mountain_subarray = subarray
                length_of_longest_mountain_subarray = len(subarray)

    return longest_mountain_subarray, length_of_longest_mountain_subarray


def find_length_of_maximum_subarray_sum_taking_the_real_part_dynamic(real_part_list):
    complex_number_list_length = len(real_part_list)

    # Initialize variables to track the maximum sum and its ending position
    maximum_sum = real_part_list[0]
    maximum_sum_ending_here = real_part_list[0]

    # Initialize variables to track the start and end indices of the maximum subarray
    start_index = 0
    end_index = 0

    for i in range(1, complex_number_list_length):
        # Update the maximum ending at the current position
        if maximum_sum_ending_here + real_part_list[i] < real_part_list[i]:
            maximum_sum_ending_here = real_part_list[i]
            start_index = i
        else:
            maximum_sum_ending_here += real_part_list[i]

        # Update the overall maximum sum and its ending position
        if maximum_sum_ending_here > maximum_sum:
            maximum_sum = maximum_sum_ending_here
            end_index = i

    # Extract the elements of the maximum subarray
    maximum_sum_subarray = real_part_list[start_index:end_index + 1]

    return maximum_sum, maximum_sum_subarray

#
# Write below this comment 
# UI section
# Write all functions that have input or print statements here
# Ideally, this section should not contain any calculations relevant to program functionalities
#


def print_menu():
    print("1. Read a list of complex numbers: ")
    print("2. Display the entire list of numbers: ")
    print("3. solve the given problem: ")
    print("4. Exit the application: ")


def read_list_of_complex_numbers():
    complex_number_list = []
    number_of_complex_numbers = int(input("How many complex numbers do you want to read? "))

    for i in range(number_of_complex_numbers):
        real_part = int(input("Write the real part: "))
        imaginary_part = int(input("Write the imaginary part: "))
        complex_number = create_complex_number(real_part, imaginary_part)
        complex_number_list.append(complex_number)

    return complex_number_list


def print_the_complex_number_list(complex_number_list):
    for complex_number in complex_number_list:
        print(convert_complex_number_to_string(complex_number))


def print_subarray_and_length_of_longest_real_part_mountain_subarray(real_part_list):
    longest_mountain_subarray, length_of_longest_mountain_subarray = find_longest_subarray_where_the_real_part_is_a_mountain(
        real_part_list)
    print("The length of the longest subarray where the real part is a mountain is: ", length_of_longest_mountain_subarray)
    print("The longest subarray where the real part is a mountain is: ", longest_mountain_subarray)


def print_subarray_and_length_of_maximum_subarray_sum_taking_the_real_part_dynamic(real_part_list):
    maximum_sum, maximum_sum_subarray = find_length_of_maximum_subarray_sum_taking_the_real_part_dynamic(real_part_list)
    print("The length of the maximum subarray sum taking the real part is: ", maximum_sum)
    print("The elements of the maximum subarray sum taking the real part are: ", maximum_sum_subarray)


def user_input():
    print_menu()
    complex_number_list = generate_complex_numbers_at_startup()
    while True:
        option = int(input("Choose an option: "))
        if option == 1:
            complex_number_list = read_list_of_complex_numbers()
        elif option == 2:
            print_the_complex_number_list(complex_number_list)
        elif option == 3:
            print_subarray_and_length_of_longest_real_part_mountain_subarray(get_real_part_list(complex_number_list))
            print_subarray_and_length_of_maximum_subarray_sum_taking_the_real_part_dynamic(get_real_part_list(complex_number_list))
        elif option == 4:
            break
        else:
            print("Invalid option!")


if __name__ == "__main__":
    user_input()
