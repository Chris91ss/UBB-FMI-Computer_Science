def find_all_partitions_of_a_set(size_of_our_set):
    """
    This function creates a sequence in the form of [a1, a2, ..., an]
    with the meaning that the k-th element belongs to the ak-th set in the partition
    Here is an example with the size equal to 4: [1, 2, 1, 2] means that {{a1, a3}, {a2, a4}}
    :param size_of_our_set: natural number, size of the input set
    :return: we don't return anything
    """
    global total_number_of_partitions
    # we basically generate the number of the partition we place each element a from the sequence
    partition_value_mask = [1 for _ in range(0, size_of_our_set)]  # the sequence [a1, a2, ..., an]

    while True:
        total_number_of_partitions += 1
        print_out_partition_and_relations(partition_value_mask)  # prints the partition

        index = size_of_our_set - 1  # index in partition_value_mask
        while index > 0:
            max_value = max(partition_value_mask[0: index])
            if partition_value_mask[index] > max_value:
                partition_value_mask[index] = 1
                index -= 1
            else:
                partition_value_mask[index] += 1
                break
        if index == 0:
            break


def print_out_partition_and_relations(partition_value_mask):
    """
    This function creates a sequence in the form of the following list [a1, a2, ..., an]
    with the meaning that the k-th element belongs to the ak-th set in the partition_values
    and prints the corresponding partition and their equivalence relations
    Here is an example with the size equal to 4: [1, 2, 1, 2] means that {{a1, a3}, {a2, a4}}
    :param partition_value_mask: list, sequence in the form of [a1, a2, ..., an] with the meaning
                                 that the k-th element belongs to the ak-th set in the partition
    :return: this function does not return anything
    """
    partition_values = [[] for _ in range(max(partition_value_mask))]  # creates and stores the partition
    for index in range(len(partition_value_mask)):
        partition_values[partition_value_mask[index] - 1].append(index + 1)

    if max(partition_value_mask) == 1:  # if the partition is in the form of {{a1, a2, a3}}
        format_partition_on_print_set(partition_values)  # format and write the partition in the file
        test_out.write("} ==> A x A")
    elif max(partition_value_mask) == len(partition_value_mask):  # if the partition is in the form: {{a1}, {a2}, {a3}}
        format_partition_on_print_set(partition_values)  # format and write the partition in the file
        test_out.write("} ==> <>A")

    else:
        format_partition_on_print_set(partition_values)  # format and write the partition in the file
        test_out.write("} ==> <>A U {")

        # here we print the equivalence relation
        first = True
        for index in range(len(partition_values)):
            if len(partition_values[index]) > 1:
                if not first:
                    test_out.write(", ")
                first = False

                for j in range(len(partition_values[index]) - 1):
                    for k in range(j + 1, len(partition_values[index])):
                        test_out.write("{" + f"a{partition_values[index][j]}, a{partition_values[index][k]}" + "}, ")
                        test_out.write("{" + f"a{partition_values[index][k]}, a{partition_values[index][j]}" + "}")
                        if j != len(partition_values[index]) - 2:
                            test_out.write(", ")

            if index == len(partition_values) - 1:
                test_out.write("}")
    test_out.write("\n")
    test_out.write("\n")


def format_partition_on_print_set(partition_values):
    """
    This function formats and prints the list [partition_values] so it appears as {{a1, a3}, {a2, a4}} instead of
    the default representation in the console [[1, 3], [2, 4]]
    :param partition_values: a list, containing the partition of the given set
    :return: we don't return anything
    """
    test_out.write("{")
    for index in range(len(partition_values)):
        for j in range(len(partition_values[index])):
            if j == 0:
                test_out.write("{")
            if j != len(partition_values[index]) - 1:
                test_out.write("a" + str(partition_values[index][j]) + ", ")
            else:
                test_out.write("a" + str(partition_values[index][j]) + "}")
        if index != len(partition_values) - 1:
            test_out.write(", ")


if __name__ == '__main__':
    test_in = open("tests_folder/test_1_input.in", 'r')
    test_out = open("tests_folder/test_1_output.out", 'w')

    size_of_a_set = int(test_in.readline())
    test_in.close()

    test_out.write("Let Delta = <>")  # because ∆ and ⇝ can not be writen in files, we switch them with <> and ==>
    test_out.write("\n")
    test_out.write("\n")
    test_out.write("Let set A = {")  # here we display the set A
    for i in range(1, size_of_a_set + 1):
        if i != size_of_a_set:
            test_out.write(f"a{i}, ")
        else:
            test_out.write(f"a{i}" + "}")
    test_out.write("\n")
    test_out.write("\n")

    if size_of_a_set == 1:  # this is an exception for size_of_a = 1
        test_out.write("{{a1}} ==> <>A")
        test_out.write("\n")
        test_out.write("\n")
        test_out.write("The number of partitions is 1")
    else:
        total_number_of_partitions = 0  # this variable holds the number of partitions after we count them
        find_all_partitions_of_a_set(size_of_a_set)
        test_out.write(f"The number of partitions is {total_number_of_partitions}")
    test_out.close()
