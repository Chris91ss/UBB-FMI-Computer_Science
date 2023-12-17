# reads and prints from files

import numpy


# ------------------#
# - Functions Here -#
# ------------------#

def get_vectors(all_vectors: list, vector: list, k: int, dimension: int):
    """
    This function gets all the vectors of (Z2)^n over Z2
    :param all_vectors: list, contains all the vectors of (Z2)^n over Z2
    :param vector: list, used to create the vectors, initially empty
    :param k: int, index in the [vector] list
    :param dimension: int, the dimension of (Z2)^n over Z2 (another name for n)
    :return: nothing
    """
    if k == dimension:
        # appends a copy of the vector (so it doesn't update later) to the all_vectors list
        copy_of_row = vector.copy()
        all_vectors.append(copy_of_row)
        return

    for j in range(0, 2):
        vector[k] = j
        get_vectors(all_vectors, vector, k + 1, dimension)


def get_bases(all_bases: list, all_vectors: list, basis: list, k: int, dimension: int):
    """
    This function gets all the bases of (Z2)^n over Z2
    :param all_bases: list, contains all the bases of (Z2)^n over Z2
    :param all_vectors: list, contains all the vectors of (Z2)^n over Z2
    :param basis: list, used to create the bases, initially empty
    :param k: int, index in the [basis] list
    :param dimension: int, the dimension of (Z2)^n over Z2 (another name for n)
    :return: nothing
    """
    global number_of_bases, vector_used

    if k == dimension:
        if linear_independent_modulo_2(basis) is True:
            number_of_bases += 1
            all_bases.append(basis.copy())

        return

    for i in range(len(all_vectors)):
        basis[k] = all_vectors[i]

        if not vector_used[i]:
            vector_used[i] = True
            get_bases(all_bases, all_vectors, basis, k + 1, dimension)
            vector_used[i] = False


def linear_independent_modulo_2(basis: list) -> bool:
    """
    This function checks if the basis is linearly independent (scalars from Z2)
    :param basis: list, contains the vectors that could form a basis
    :return: bool, True if the basis is linearly independent
                   False otherwise
    """
    global vector_mask

    for index_basis in range(len(basis)):
        vector = basis[index_basis]

        for mask in vector_mask:
            vectors_to_add = []

            for index_mask in range(len(mask)):
                if mask[index_mask] == 1 and index_basis != index_mask:
                    vectors_to_add.append(basis[index_mask])

            if vectors_to_add:
                result = add_vectors_modulo_2(vectors_to_add)

                if result == vector:
                    return False

    return True


def add_vectors_modulo_2(vectors: list) -> list:
    """
    This function adds the vectors in Z2
    :param vectors: list, contains the vectors to be added
    :return: list, sum of the vectors
    """
    result = vectors[0]
    for i in range(1, len(vectors)):
        result = numpy.add(result, vectors[i])

    returned_result = []
    for i in range(len(result)):
        returned_result.append(result[i] % 2)

    return returned_result

# -------------#
# - Test Here -#
# -------------#

def test_create_vectors():
    test_vectors = []
    get_vectors(test_vectors, [0 for _ in range(1)], 0, 1)
    assert test_vectors == [[0], [1]]

    test_vectors = []
    get_vectors(test_vectors, [0 for _ in range(2)], 0, 2)
    assert test_vectors == [[0, 0], [0, 1], [1, 0], [1, 1]]

    test_vectors = []
    get_vectors(test_vectors, [0 for _ in range(3)], 0, 3)
    assert test_vectors == [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

    test_vectors = []
    get_vectors(test_vectors, [0 for _ in range(4)], 0, 4)
    assert test_vectors == [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1],
                            [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
                            [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]


# ---------------#
# - Output Here -#
# ---------------#

def print_bases(all_bases: list, number_of_bases: int):
    test_out = open(file_name + 'output.out', 'w')

    test_out.write(f"The number of bases of the vector space (Z2)^{n} over Z2 is {number_of_bases}\n")

    test_out.write("\nThe vectors of each such basis are :\n\n")
    for basis in all_bases:
        test_out.write(str(basis))
        test_out.write("\n")

    test_out.close()


# --------------#
# - Start Here -#
# --------------#

if __name__ == '__main__':
    file_name = 'tests/test_2_'

    vectors = []
    bases = []
    number_of_bases = 0

    test_in = open(file_name + 'input.in', 'r')
    n = int(test_in.readline())
    test_in.close()

    get_vectors(vectors, [0 for _ in range(n)], 0, n)
    vectors = vectors[1:]  # get rid of the 0 vector

    vector_used = [False for _ in range(len(vectors))]
    vector_mask = vectors[:-1]  # mask used to check if a vector is the sum of others
                                # (if it is, it's not a basis, because it's not linearly independent)

    get_bases(bases, vectors, [0 for _ in range(n)], 0, n)

    print_bases(bases, number_of_bases)
