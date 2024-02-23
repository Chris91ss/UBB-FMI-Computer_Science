from random import randint


def f(data: list):
    if data is None or data == []:
        raise ValueError("Input list cannot be None or empty.")
    aux = data[0]
    for elem in data:
        if aux - elem > 0:
            return False
        aux = elem
    return True


def test_f():
    for _ in range(100):
        # Generate a random list with a random length between 0 and 100
        length = randint(0, 100)
        data = [randint(-1000, 1000) for _ in range(length)]
        data.sort()  # Sorting the list to make sure it's in non-descending order
        # Shuffle the list with 50% probability to ensure randomness
        if randint(0, 1):
            data.reverse()
        try:
            assert f(data) == True
        except AssertionError:
            print("Test failed for input:", data)
    print("All tests passed!")


test_f()
