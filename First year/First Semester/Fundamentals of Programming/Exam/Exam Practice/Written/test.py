class Testing:
    def __init__(self):
        self.__data = [1, 2, 3]

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __add__(self, other):
        return self.__data[0] + other.__data[0]


data = Testing()
data2 = Testing()
data[0] = 5
print(data + data2)
print(data[0], data[1], data[2])
