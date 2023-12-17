import numpy


# ------------------#
# ------------------#
# ------------------#

def get_vectors(n: int) -> list:
    """
    This function returns all the possible vectors of length n, with elements 0 or 1
    :param n: int, the length of the vectors
    :return: list, a list of all the possible vectors
    """

    vectors = []
    get_vectors_implementation(vectors, [0] * n, 0, n)
    return vectors


def get_vectors_implementation(vectors: list, current_vector: list, current_index, n: int):
    if current_index == n:
        vectors.append(current_vector.copy())
        return None

    for i in range(0, 2):  # backtracking algorithm to get all the possible vectors
        current_vector[current_index] = i
        get_vectors_implementation(vectors, current_vector, current_index + 1, n)


# ------------------#
# ------------------#
# ------------------#

def get_all_masks(k: int) -> list:
    """
    This function returns all the possible masks with maximum element k - 1, (0, 1, 2, ..., k - 1)
    :param k: int, the maximum element of the mask
    :return: list, a list of all the possible masks
    """

    masks = []
    get_all_masks_implementation(masks, k, 0, [])

    return masks


def get_all_masks_implementation(masks: list, k: int, index: int, mask: list):
    while index < k:  # backtracking algorithm to get all the possible masks
        mask.append(index)
        masks.append(mask.copy())
        get_all_masks_implementation(masks, k, index + 1, mask)
        mask.pop()
        index += 1


# ------------------#
# ------------------#
# ------------------#

def get_basis(all_masks: list, all_spans: list, all_basis: list,
              basis: list, used_vectors: list, i: int, vectors: list, k: int, n: int):
    """
    This gets all the possible bases for the subspaces
    :param all_masks: list, contains all the possible masks
    :param all_spans: list, contains all the possible spans
    :param all_basis: list, contains all the possible bases

    :param basis: list, contains the vectors that could form a basis
    :param used_vectors: list, contains the vectors that are already used
    :param i: int, the index of the vector that was last used
    :param vectors: list, contains all the possible vectors
    :param k: int, the number of vectors in the basis
    :param n: int, the length of the vectors
    """

    if len(basis) == k:  # if the basis is complete
        if check_if_basis(all_masks, all_spans, basis, n, k):  # if the basis is correct
            all_basis.append(basis.copy())  # add the basis to the list of all the possible bases
            all_spans.append(basis.copy())  # add the basis to the list of all the possible spans

        return None

    for j in range(i + 1, len(vectors)):  # backtracking algorithm to get all the possible bases
        if j not in used_vectors:
            basis.append(vectors[j])
            used_vectors.append(j)

            get_basis(all_masks, all_spans, all_basis,
                      basis, used_vectors, j, vectors, k, n)

            basis.pop()
            used_vectors.pop()


def check_if_basis(all_masks: list, all_spans: list, basis: list, n: int, k: int) -> bool:
    """
    This function checks if the basis is a basis for the subspace
    :param all_masks: list, contains all the possible masks
    :param all_spans: list, contains all the possible spans
    :param basis: list, contains the vectors that could form a basis
    :param n: int, the length of the vectors
    :param k: int, the number of vectors in the basis
    """

    if not is_linearly_independent(basis):
        return False

    for span in all_spans:
        vectors_used = []

        for mask in all_masks:  # check for each mask
            result = [0 for _ in range(n)]

            for index in mask:  # get the vectors from the mask and add them
                for i in range(n):
                    result[i] += span[index][i]
                    result[i] %= 2

            for index in range(k):  # check if the result is in the basis
                if result == basis[index] and index not in vectors_used:  # if the result is in the basis
                    vectors_used.append(index)  # add the index of the vector to the list of used vectors

            if len(vectors_used) == k:  # if all the vectors were used
                return False  # the basis is not a basis

    return True


# ------------------#
# ------------------#
# ------------------#

def is_linearly_independent(basis: list) -> bool:
    """
    This function checks if the basis is linearly independent (scalars from Z2)
    :param basis: list, contains the vectors that could form a basis
    :return: bool, True if the basis is linearly independent
                   False otherwise
    """

    addition_masks = get_vectors(len(basis))
    addition_masks = addition_masks[1:]  # remove the zero vector
    # masks used for the addition of the vectors

    for index_basis in range(len(basis)):
        vector = basis[index_basis]

        for mask in addition_masks:  # check for each mask if the vectors that correspond to it add up to another vector
            vectors_to_add = []

            for index_mask in range(len(mask)): # get the vectors from the mask
                if mask[index_mask] == 1 and index_basis != index_mask:
                    vectors_to_add.append(basis[index_mask])

            if vectors_to_add:  # if there are vectors to add / mask is not all zeros
                result = add_vectors_modulo_2(vectors_to_add)  # add the vectors

                if result == vector:  # if the result is the same as the vector
                    return False  # the basis is not linearly independent

    # if we didn't find any vectors that add up to another vector
    # the basis is linearly independent
    return True


def add_vectors_modulo_2(vectors: list) -> list:
    """
    This function adds the vectors in Z2
    :param vectors: list, contains the vectors to be added
    :return: list, sum of the vectors
    """
    result = vectors[0]
    for i in range(1, len(vectors)):
        result = numpy.add(result, vectors[i])  # add the vectors normally

    returned_result = []
    for i in range(len(result)):
        returned_result.append(result[i] % 2)  # apply modulo 2 on the result

    return returned_result


# ------------------#
# ------------------#
# ------------------#

def print_solution(all_bases: list):
    print(f"The number of {k}-dimensional subspaces of the vector space (Z2)^{n} over Z2 is {len(all_bases)}.")

    print("\nA basis of each such subspace is :\n")
    for basis in all_bases:
        print(f"{basis}\n")


# ------------------#
# ------------------#
# ------------------#

def get_integers() -> tuple[int, int]:
    try:
        k = int(input("k = "))
        n = int(input("n = "))

        if k not in range(1, 7) or n not in range(1, 7) or k > n:
            raise ValueError

        return k, n

    except ValueError:
        print("Invalid input!")
        return get_integers()


# ------------------#
# ------------------#
# ------------------#


if __name__ == '__main__':
    k, n = get_integers()  # get the input

    all_vectors = get_vectors(n)
    all_vectors = all_vectors[1:]  # remove the zero vector

    all_masks = get_all_masks(k)  # get all the possible masks
    # will be used for addition of vectors
    # of form [0], [0, 1] ; meaning vector on index 0, respectively vector on index 0 and vector on index 1

    all_spans = []
    all_basis = []
    for i in range(len(all_vectors)):
        basis = []
        used_vectors = [i]
        basis.append(all_vectors[i])
        get_basis(all_masks, all_spans, all_basis,
                  basis, used_vectors, i, all_vectors, k, n)

    print_solution(all_basis)  # print the solution
