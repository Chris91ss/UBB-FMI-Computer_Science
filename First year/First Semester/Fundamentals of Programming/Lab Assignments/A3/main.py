import timeit
from random import randint


def print_menu():
    """
    this function prints the menu of our console driven application
    """
    print("1. Generate a list of n natural numbers")
    print("2. Sort this list using Bubble Sort")
    print("3. Sort this list using Heap Sort")
    print("4. Display on a table how the algorithms behave during the Best Case")
    print("5. Display on a table how the algorithms behave during the Average Case")
    print("6. Display on a table how the algorithms behave during the Worst Case")
    print("7. Exit the program")


def generate_random_numbers(number_of_random_values):
    """
    this function generates number_of_random_values natural random numbers that are part of the interval [0, 100]
    """
    list_of_numbers = []

    for i in range(0, number_of_random_values):
        list_of_numbers.append(randint(0, 100))

    return list_of_numbers


def generate_sorted_list(number_of_values):
    """
    This function generateS n natural random numbers that are part of the interval [0, 100] and are in increasing order
    """
    list_of_numbers = generate_random_numbers(number_of_values)
    list_of_numbers.sort()
    return list_of_numbers


def generate_reverse_sorted_list(number_of_values):
    """
    This function generates n natural random numbers that are part of the interval [0, 100] and are in decreasing order
    """
    list_of_numbers = generate_sorted_list(number_of_values)
    list_of_numbers.reverse()
    return list_of_numbers


def print_list_after_step(list_of_numbers, step):
    """
    this function during sorting, will display the partially sorted list on the
    console each time it makes step operations or passes
    """
    print("Step", step, ": ", list_of_numbers)


def bubble_sort(list_of_numbers, step):
    """
    this function traverses a list and compares adjacent values,
    swapping them if they are not in the correct order
    sorting the list in the end

    Complexity -> O(n^2)
    """
    swapped = False
    length_of_list = len(list_of_numbers)
    index_of_step = 0
    total_of_steps = 0
    # Traverse through all array elements
    for i in range(length_of_list - 1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, length_of_list - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if list_of_numbers[j] > list_of_numbers[j + 1]:
                swapped = True
                list_of_numbers[j], list_of_numbers[j + 1] = list_of_numbers[j + 1], list_of_numbers[j]

                index_of_step += 1
                total_of_steps += 1
                if index_of_step == step:
                    print_list_after_step(list_of_numbers, total_of_steps)
                    index_of_step = 0

        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return

    return list_of_numbers


def heapify(list_of_numbers, length_of_list, i):  # Rearrange a heap to maintain the heap property
    """
    this function converts the input array into a max heap
    """
    largest_value = i  # Initialize largest as root
    left_child = 2 * i + 1  # left = 2*i + 1
    right_child = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root

    if left_child < length_of_list and list_of_numbers[i] < list_of_numbers[left_child]:
        largest_value = left_child

    # See if right child of root exists and is
    # greater than root

    if right_child < length_of_list and list_of_numbers[largest_value] < list_of_numbers[right_child]:
        largest_value = right_child

    # Change root, if needed

    if largest_value != i:  # swap
        (list_of_numbers[i], list_of_numbers[largest_value]) = (list_of_numbers[largest_value], list_of_numbers[i])

        # Heapify the root.

        heapify(list_of_numbers, length_of_list, largest_value)


def heap_sort(list_of_numbers, step):
    """
    this function efficiently sorts an array by creating a max heap and repeatedly extracting
    the maximum element from it

    Complexity -> O(n log n)
    """
    length_of_list = len(list_of_numbers)
    index_of_step = 0
    total_of_steps = 0
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(length_of_list // 2 - 1, -1, -1):
        heapify(list_of_numbers, length_of_list, i)

    # One by one extract elements

    for i in range(length_of_list - 1, 0, -1):
        (list_of_numbers[i], list_of_numbers[0]) = (list_of_numbers[0], list_of_numbers[i])  # swap
        heapify(list_of_numbers, i, 0)

        total_of_steps += 1
        index_of_step += 1
        if index_of_step == step:
            print_list_after_step(list_of_numbers, total_of_steps)
            index_of_step = 0

    return list_of_numbers


def build_table_with_time_results_bubble_sort(list_of_numbers, number_of_values_in_list):
    start_iteration_time = timeit.default_timer()
    bubble_sort(list_of_numbers, 0)
    end_interation_time = timeit.default_timer()

    total_time = end_interation_time - start_iteration_time  # get the time of execution

    total_time_string = "{:.8f}".format(total_time)  # format the time to a string with 8 fixed decimals

    print("Data structure of ", number_of_values_in_list, " elements\n", "Milliseconds -> ",
          total_time_string)
    print("\n")


def build_table_with_time_results_heap_sort(list_of_numbers, number_of_values_in_list):
    start_iteration_time = timeit.default_timer()
    heap_sort(list_of_numbers, 0)
    end_interation_time = timeit.default_timer()

    total_time = end_interation_time - start_iteration_time  # get the time of execution

    total_time_string = "{:.8f}".format(total_time)  # format the time to a string with 8 fixed decimals

    print("Data structure of ", number_of_values_in_list, " elements\n", "Milliseconds -> ",
          total_time_string)
    print("\n")


def solve_problem():
    """
    this function is where the program is executed
    """
    print_menu()
    list_of_numbers = []
    while True:
        option = int(input("Select an option: "))
        if option == 1:
            number_of_random_values = int(input("Choose a value for number_of_random_values: "))
            list_of_numbers = generate_random_numbers(number_of_random_values)
            print(list_of_numbers)
        elif option == 2:
            step = int(input("Choose a value for the step: "))
            list_of_numbers = bubble_sort(list_of_numbers, step)
            print("After sorting, the sorted list is", list_of_numbers)
        elif option == 3:
            step = int(input("Choose a value for the step: "))
            list_of_numbers = heap_sort(list_of_numbers, step)
            print("After sorting, the sorted list is", list_of_numbers)
        elif option == 4:
            print("The best case is when the array is already sorted")
            print("The complexity for bubble sort in this case is O(n)")
            print("BUBBLE SORT TIME: \n")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_sorted_list(number_of_values_in_list)
                build_table_with_time_results_bubble_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2

            print("HEAP SORT TIME: \n")
            print("The complexity for heap sort in this case is O(n*log(n))")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_sorted_list(number_of_values_in_list)
                build_table_with_time_results_heap_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2
        elif option == 5:
            print("The average case is when the array is generated randomly")
            print("The complexity for bubble sort in this case is O(n^2)")
            print("BUBBLE SORT TIME: \n")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_random_numbers(number_of_values_in_list)
                build_table_with_time_results_bubble_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2

            print("HEAP SORT TIME: \n")
            print("The complexity for heap sort in this case is O(n*log(n))")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_random_numbers(number_of_values_in_list)
                build_table_with_time_results_heap_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2
        elif option == 6:
            print("The worst case is when the array is sorted in inverse order")
            print("The complexity for bubble sort in this case is O(n^2)")
            print("BUBBLE SORT TIME: \n")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_reverse_sorted_list(number_of_values_in_list)
                build_table_with_time_results_bubble_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2

            print("HEAP SORT TIME: \n")
            print("The complexity for heap sort in this case is O(n*log(n))")
            number_of_values_in_list = 500
            for i in range(5):
                list_of_numbers = generate_reverse_sorted_list(number_of_values_in_list)
                build_table_with_time_results_heap_sort(list_of_numbers, number_of_values_in_list)
                number_of_values_in_list = number_of_values_in_list * 2
        elif option == 7:
            print("Program has exited successfully")
            break
        else:
            print("ERROR. -> You must choose a value from 1 to 7")


solve_problem()
