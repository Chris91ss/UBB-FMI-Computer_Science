import functions


def test_create_complex_number():
    assert functions.create_complex_number(1, 2) == [1, 2]
    assert functions.create_complex_number(0, 0) == [0, 0]
    assert functions.create_complex_number(-1, -2) == [-1, -2]
    assert functions.create_complex_number(-1, 0) == [-1, 0]
    assert functions.create_complex_number(-1, -1) == [-1, -1]


def test_get_real_part():
    assert functions.get_real_part([1, 2]) == 1
    assert functions.get_real_part([0, 0]) == 0
    assert functions.get_real_part([-1, -2]) == -1
    assert functions.get_real_part([1, -2]) == 1


def test_get_imaginary_part():
    assert functions.get_imaginary_part([1, 2]) == 2
    assert functions.get_imaginary_part([0, 0]) == 0
    assert functions.get_imaginary_part([-1, -2]) == -2
    assert functions.get_imaginary_part([-1, 2]) == 2


def test_get_operation_type():
    assert functions.get_operation_type(['add', [1, 2]]) == 'add'
    assert functions.get_operation_type(['insert', [1, 2]]) == 'insert'
    assert functions.get_operation_type(['remove', [1, 2]]) == 'remove'


def test_get_operation_data():
    assert functions.get_operation_data(['add', [1, 2]]) == [1, 2]
    assert functions.get_operation_data(['insert', [1, 2]]) == [1, 2]
    assert functions.get_operation_data(['remove', [1, 2]]) == [1, 2]


def test_set_real_part():
    complex_number = [1, 2]
    functions.set_real_part(complex_number, 3)
    assert complex_number == [3, 2]
    complex_number = [0, 0]
    functions.set_real_part(complex_number, 3)
    assert complex_number == [3, 0]
    complex_number = [-1, -2]
    functions.set_real_part(complex_number, 3)
    assert complex_number == [3, -2]
    complex_number = [-1, -1]
    functions.set_real_part(complex_number, 3)
    assert complex_number == [3, -1]


def test_set_imaginary_part():
    complex_number = [1, 2]
    functions.set_imaginary_part(complex_number, 3)
    assert complex_number == [1, 3]
    complex_number = [0, 0]
    functions.set_imaginary_part(complex_number, 3)
    assert complex_number == [0, 3]
    complex_number = [-1, -2]
    functions.set_imaginary_part(complex_number, 3)
    assert complex_number == [-1, 3]
    complex_number = [-1, -1]
    functions.set_imaginary_part(complex_number, 3)
    assert complex_number == [-1, 3]


def test_add_complex_number():
    assert functions.add_complex_number(1, 2, [[1, 2]]) == [[1, 2], [1, 2]]
    assert functions.add_complex_number(1, 2, [[0, 0]]) == [[0, 0], [1, 2]]
    assert functions.add_complex_number(1, 2, [[-1, -2]]) == [[-1, -2], [1, 2]]
    assert functions.add_complex_number(1, 2, [[-1, 0]]) == [[-1, 0], [1, 2]]
    assert functions.add_complex_number(1, 2, [[-1, -1]]) == [[-1, -1], [1, 2]]


def test_insert_complex_number():
    assert functions.insert_complex_number(1, 2, 0, [[1, 2]]) == [[1, 2], [1, 2]]
    assert functions.insert_complex_number(1, 2, 0, [[0, 0]]) == [[1, 2], [0, 0]]
    assert functions.insert_complex_number(1, 2, 0, [[-1, -2]]) == [[1, 2], [-1, -2]]
    assert functions.insert_complex_number(1, 2, 0, [[-1, 0]]) == [[1, 2], [-1, 0]]
    assert functions.insert_complex_number(1, 2, 0, [[-1, -1]]) == [[1, 2], [-1, -1]]


def test_remove_number_from_position():
    assert functions.remove_number_from_position(0, [[1, 2]]) == []
    assert functions.remove_number_from_position(0, [[0, 0]]) == []
    assert functions.remove_number_from_position(0, [[-1, -2]]) == []
    assert functions.remove_number_from_position(0, [[-1, 0]]) == []
    assert functions.remove_number_from_position(0, [[-1, -1]]) == []


def test_remove_number_from_interval():
    assert functions.remove_number_from_interval(0, 1, [[1, 2], [2, 3]]) == []
    assert functions.remove_number_from_interval(0, 1, [[0, 0], [0, 0]]) == []
    assert functions.remove_number_from_interval(0, 0, [[-1, -2]]) == []


def test_replace_number_from_position():
    assert functions.replace_number_from_position(1, 2, 0, [[1, 2]]) == [[1, 2]]
    assert functions.replace_number_from_position(1, 2, 0, [[0, 0]]) == [[1, 2]]
    assert functions.replace_number_from_position(1, 2, 0, [[-1, -2]]) == [[1, 2]]


def test_filter_real_part():
    assert functions.filter_list_of_complex_numbers_by_real_part([[1, 2], [2, 3]]) == []
    assert functions.filter_list_of_complex_numbers_by_real_part([[1, 0], [1, 0]]) == [[1, 0], [2, 0]]


def test_filter_modulo():
    assert functions.filter_list_of_complex_numbers_by_modulo_less_than_value([[3, 4], [10, 10]], 10) == [[3, 4]]
    assert functions.filter_list_of_complex_numbers_by_modulo_equal_to_value([[6, 8], [10, 10]], 10) == [[6, 8]]
    assert functions.filter_list_of_complex_numbers_by_modulo_greater_than_value([[10, 6], [1, 1]], 10) == [[10, 6]]


def run_all_tests():
    test_create_complex_number()
    test_get_real_part()
    test_get_imaginary_part()
    test_get_operation_type()
    test_get_operation_data()
    test_set_real_part()
    test_set_imaginary_part()
    test_add_complex_number()
    test_insert_complex_number()
    test_remove_number_from_position()
    test_remove_number_from_interval()
    test_replace_number_from_position()
    test_filter_real_part()
    test_filter_modulo()

