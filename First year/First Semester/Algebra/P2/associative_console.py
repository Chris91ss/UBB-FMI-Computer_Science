# reads and prints from the console


def print_matrix(matrix):
    """
    This function prints a matrix
    :param matrix: matrix to be printed
    :return: nothing
    """
    for i in range(n):
        for j in range(n):
            print(f"a{str(matrix[i][j])} ", end='')
        print()
    print()


def find_rows(k):
    """
    This function finds all possible lists composed of elements from A that will serve as rows in the operation tables
    using a backtracking method
    :param k: natural number < n that represents the current position in the list it creates
    :return: nothing
    """
    if k > n - 1:
        copy_of_row = row.copy()  # appends a copy of the row (so it doesn't update later) to the all_rows list
        all_rows.append(copy_of_row)
        return

    for j in range(1, n + 1):
        row[k] = j
        find_rows(k + 1)


def find_tables(k):
    """
    This function finds all possible matrices composed of lists created by find_row using a backtracking method
    It also checks if a matrix corresponds to the operation table of an associative operation and if so prints it and
    counts how many such operation tables there are
    :param k: natural number < n that represents the current column in the matrix it creates
    :return: nothing
    """
    global number_of_associative_operations

    if k > n - 1:
        is_associative = True
        for x in range(n):  # checks if the operation is associative
            if not is_associative:
                break
            for y in range(n):
                if not is_associative:
                    break
                for z in range(n):
                    if not is_associative:
                        break
                    if operation_table[operation_table[x][y] - 1][z] != operation_table[x][operation_table[y][z] - 1]:
                        is_associative = False
                        break

        if is_associative:
            number_of_associative_operations += 1
            print_matrix(operation_table)

        return

    for element in all_rows:
        operation_table[k] = element
        find_tables(k + 1)


if __name__ == '__main__':

    n = int(input("Enter number n : "))

    print("Let set A = {", end='')  # this displays the set A
    for i in range(1, n + 1):
        if i != n:
            print(f"a{i}, ", end='')
        else:
            print(f"a{i}" + "}")
    print()

    row = [0 for i in range(n)]  # represents a list composed of elements from A that can repeat
    all_rows = []  # list of lists that saves all possible rows
    find_rows(0)

    operation_table = [[0 for i in range(n)] for j in range(n)]  # represents an operation table
    number_of_associative_operations = 0  # keeps count of the number of associative operations

    print("The operation tables of the associative operations on set A are given by the matrices : ")
    print()
    find_tables(0)

    print(f"The number of associative operations on set A is : {number_of_associative_operations}")
