# The sequence a1, ..., an of distinct integer numbers is given. Display all subsets with a mountain aspect.
# A set has a mountain aspect if the elements increase up to a point and then they decrease. E.g. 10, 16, 27, 18, 14, 7.

def solve_problem():
    """
    Both versions need to explore and store all 2^n subsets so in conclusion =>
    both have the same Time complexity O(n * 2^n)
    O(n) because for each subset we perform a check to see if it's a mountain
    O(2^n) - recursive - we have 2^n recursive calls, where n is the

    Space complexity:
    recursive - O(n) - the recursion stack depth being n in the worst case
    iterative - O(n * 2^n) because we need to generate and store all 2^n subsets of the input list each taking O(n)
    """
    given_input_list = input("Write a list of numbers: ")
    given_list_of_numbers = list(map(int, given_input_list.split(' ')))

    print("Using the recursive implementation, the generated arrays are")
    find_mountain_subsets_recursive(given_list_of_numbers, [], 0)
    print("Using the iterative implementation, the generated arrays are")
    find_mountain_subsets_iterative(given_list_of_numbers)


def is_a_mountain_subset(subset):
    length_of_subset = len(subset)

    # A mountain should have at least 3 elements
    if length_of_subset < 3:
        return False

    # Find the peak of the mountain
    peak = max(subset)
    peak_index = subset.index(peak)

    # If the peak is the first or last element, it's not a mountain
    if peak_index == 0 or peak_index == length_of_subset - 1:
        return False

    # Check if the first part is increasing
    for i in range(peak_index):
        if subset[i] >= subset[i + 1]:
            return False

    # Check if the second part is decreasing
    for i in range(peak_index, length_of_subset - 1):
        if subset[i] <= subset[i + 1]:
            return False

    return True


def find_mountain_subsets_recursive(given_list_of_numbers, current_subset, current_position):
    if current_position == len(given_list_of_numbers):
        # Check if the generated subset is a mountain
        if is_a_mountain_subset(current_subset):
            print(current_subset)
        return

    # Include the current element
    current_subset.append(given_list_of_numbers[current_position])
    find_mountain_subsets_recursive(given_list_of_numbers, current_subset, current_position + 1)

    # Exclude the current element
    current_subset.pop()
    find_mountain_subsets_recursive(given_list_of_numbers, current_subset, current_position + 1)


def find_mountain_subsets_iterative(given_list_of_numbers):
    stack = []  # we are going to mimic the recursive calls using a stack
    length_of_list = len(given_list_of_numbers)
    stack.append(([], 0))  # Initial state: empty subset and current position

    while stack:
        current_subset, current_position = stack.pop()

        if current_position == length_of_list:
            # Check if the generated subset is a mountain
            if is_a_mountain_subset(current_subset):
                print(current_subset)
        else:
            # Include the current element
            included_subset = current_subset + [given_list_of_numbers[current_position]]
            stack.append((included_subset, current_position + 1))

            # Exclude the current element
            stack.append((current_subset, current_position + 1))


solve_problem()
