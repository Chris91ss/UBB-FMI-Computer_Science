# Determine the longest common subsequence of two given sequences. Subsequence elements are not required to occupy
# consecutive positions. For example, if X = "MNPNQMN" and Y = "NQPMNM", the longest common subsequence has length 4,
# and can be one of "NQMN", "NPMN" or "NPNM". Determine and display both the length of the longest common subsequence
# and at least one such subsequence.

from pprint import pprint


def find_longest_common_subsequence_dynamic(first_sequence, second_sequence, dynamic_programming_table):
    solution = ""
    length_of_first_sequence = len(first_sequence) - 1
    length_of_second_sequence = len(second_sequence) - 1

    while length_of_first_sequence:
        if first_sequence[length_of_first_sequence] == second_sequence[length_of_second_sequence]:
            solution = first_sequence[length_of_first_sequence] + solution
            length_of_first_sequence -= 1
            length_of_second_sequence -= 1
        elif (dynamic_programming_table[length_of_first_sequence - 1][length_of_second_sequence]
              < dynamic_programming_table[length_of_first_sequence][length_of_second_sequence - 1]):
            length_of_second_sequence -= 1
        else:
            length_of_first_sequence -= 1

    return solution


def compute_dynamic_programming_table(first_sequence, second_sequence):

    dynamic_programming_table = [[0 for _ in range(len(first_sequence) + 1)] for _ in range(len(second_sequence) + 1)]

    for i in range(0, len(first_sequence)):
        for j in range(0, len(second_sequence)):
            if first_sequence[i] == second_sequence[j]:
                dynamic_programming_table[i][j] = dynamic_programming_table[i - 1][j - 1] + 1
            else:
                dynamic_programming_table[i][j] = max(dynamic_programming_table[i - 1][j], dynamic_programming_table[i][j - 1])
            pprint(dynamic_programming_table)
            print("\n")

    return dynamic_programming_table


def find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length, second_sequence_length):
    if first_sequence_length == 0 or second_sequence_length == 0:
        return 0
    elif first_sequence[first_sequence_length - 1] == second_sequence[second_sequence_length - 1]:
        return 1 + find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length - 1,
                                                                second_sequence_length - 1)
    else:
        return max(
            find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length,
                                                         second_sequence_length - 1),
            find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length - 1,
                                                         second_sequence_length))


def find_longest_common_subsequence_naive(first_sequence, second_sequence, first_sequence_length, second_sequence_length):
    if first_sequence_length == 0 or second_sequence_length == 0:
        return ""
    if first_sequence[first_sequence_length - 1] == second_sequence[second_sequence_length - 1]:
        return find_longest_common_subsequence_naive(first_sequence, second_sequence, first_sequence_length - 1,
                                                     second_sequence_length - 1) + first_sequence[first_sequence_length - 1]
    if (find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length - 1, second_sequence_length)
            > find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length,
                                                           second_sequence_length - 1)):
        return find_longest_common_subsequence_naive(first_sequence, second_sequence, first_sequence_length - 1, second_sequence_length)
    else:
        return find_longest_common_subsequence_naive(first_sequence, second_sequence, first_sequence_length, second_sequence_length - 1)


def solve_and_display_results():
    first_sequence = input("first sequence is: ")
    second_sequence = input("second sequence is: ")

    dynamic_programming_table = compute_dynamic_programming_table(first_sequence, second_sequence)

    print("Dynamic programming version: ")

    print("The length of the longest common subsequence of the arrays is ",
          dynamic_programming_table[len(first_sequence) - 1][len(second_sequence) - 1])
    print("One of the longest common subsequences of the arrays is ",
          find_longest_common_subsequence_dynamic(first_sequence, second_sequence, dynamic_programming_table))

    print("Naive, non-optimized version: ")
    first_sequence_length = len(first_sequence)
    second_sequence_length = len(second_sequence)
    print("The length of the longest common subsequence of the arrays is ",
          find_longest_common_subsequence_length_naive(first_sequence, second_sequence, first_sequence_length, second_sequence_length))
    print("One of the longest common subsequences of the arrays is ",
          find_longest_common_subsequence_naive(first_sequence, second_sequence, first_sequence_length, second_sequence_length))


solve_and_display_results()
