def get_rows(all_rows: list, row: list, k: int, number_of_columns: int):
    """
    This function finds all possible lists composed of elements from Z2 that will serve as rows in the matrices
    using a backtracking method
    :param all_rows: list, contains all the rows composed of elements from Z2
    :param row: list, used to create the rows, initially empty
    :param k: int, index in the [row] list
    :param number_of_columns: int, the number of columns in the matrix
    :return: nothing
    """
    if k == number_of_columns:
        # appends a copy of the row (so it doesn't update later) to the all_rows list
        copy_of_row = row.copy()
        all_rows.append(copy_of_row)
        return

    for j in range(0, 2):
        row[k] = j
        get_rows(all_rows, row, k + 1, number_of_columns)


def get_matrices(all_matrices: list, all_rows: list, matrix: list, k: int, number_of_rows: int, number_of_columns: int):
    """
    This function finds all the matrices in reduced echelon form using a backtracking method
    :param all_matrices: list, contains all the matrices in reduced echelon form
    :param all_rows: list, contains all the rows composed of elements from Z2
    :param matrix: list, used to create the matrices, initially empty
    :param k: int, index in the [matrix] list
    :param number_of_rows: int, the number of rows in the matrix
    :param number_of_columns: int, the number of columns in the matrix
    """
    global number_of_matrices_in_reduced_echelon_form

    if k == number_of_rows:
        if check_matrix(matrix, number_of_rows, number_of_columns):
            number_of_matrices_in_reduced_echelon_form += 1
            all_matrices.append(matrix.copy())

        return

    for row in all_rows:
        matrix[k] = row
        get_matrices(all_matrices, all_rows, matrix, k + 1, number_of_rows, number_of_columns)


def check_matrix(matrix: list, number_of_rows: int, number_of_columns: int) -> bool:
    """
    This function checks if a matrix is in reduced echelon form
    :param matrix: list, the matrix to be checked
    :param number_of_rows: int, the number of rows in the matrix
    :param number_of_columns: int, the number of columns in the matrix
    :return: True if the matrix is in reduced echelon form,
             False otherwise
    """
    # this list will have the next meaning:
    # leading_ones[i] = the column on witch it has a leading one on the row i
    # -1 if the row doesn't have a leading one
    leading_ones = [-1 for _ in range(number_of_rows)]

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            if matrix[i][j] == 1:
                if leading_ones[i] == -1:
                    leading_ones[i] = j
                else:
                    return False

                break

    # check if there is a gap between the rows with leading ones
    zero_row = False
    for i in range(number_of_rows):
        if leading_ones[i] == -1:
            zero_row = True
        elif zero_row:
            return False

    # check if the leading ones are on the right side of the previous ones
    for i in range(number_of_rows):
        if leading_ones[i] != -1:
            for j in range(i):
                if leading_ones[j] > leading_ones[i]:
                    return False

    # check if a column with a leading one has only zeros everywhere else
    for i in range(number_of_rows):
        if leading_ones[i] != -1:
            for j in range(number_of_rows):
                if j != i and matrix[j][leading_ones[i]] != 0:
                    return False

    return True


# ------------------#
# ------------------#
# ------------------#

def print_matrices(all_matrices: list, number_of_matrices: int):
    test_out = open(file_name + 'output.out', 'w')

    test_out.write(f"The number of matrices in reduced echelon form is: {number_of_matrices}\n")

    test_out.write("\nThe matrices in reduced echelon form are: \n")
    for matrix in all_matrices:
        test_out.write("\n")
        for row in matrix:
            test_out.write('\t'.join(map(str, row)) + '\n')
        test_out.write("\n")


# ------------------#
# ------------------#
# ------------------#

def get_integers() -> tuple[int, int]:
    test_in = open(file_name + 'input.in', 'r')
    lines = test_in.readlines()
    number_of_rows = int(lines[0])
    number_of_columns = int(lines[1])
    test_in.close()

    if number_of_rows not in range(2, 6) or number_of_columns not in range(2, 6):
        print("Invalid input")
        exit(0)

    return number_of_rows, number_of_columns


# ------------------#
# ------------------#
# ------------------#

if __name__ == '__main__':
    file_name = 'tests/test_2_'

    rows = []
    matrices_in_reduced_echelon_form = []
    number_of_matrices_in_reduced_echelon_form = 0

    m, n = get_integers()

    get_rows(rows, [0 for _ in range(n)], 0, n)
    get_matrices(matrices_in_reduced_echelon_form, rows, [0 for _ in range(m)], 0, m, n)
    matrices_in_reduced_echelon_form = matrices_in_reduced_echelon_form[::-1]

    print_matrices(matrices_in_reduced_echelon_form, number_of_matrices_in_reduced_echelon_form)
