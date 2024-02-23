class SparseList:
    def __init__(self):
        self.data = {}
    #    self.index = -1

    def __setitem__(self, index, value):
        self.data[index] = value

    def __getitem__(self, index):
        if index in self.data:
            return self.data[index]
        else:
            return 0

    def __iter__(self):
        return SparseListIterator(self.data)

    # def __iter__(self):
    #    return self

    # def __next__(self):
    #    self.index += 1
    #    if self.index >= len(self.data):
    #        raise StopIteration
    #    return self.data[self.index]


class SparseListIterator:
    def __init__(self, data):
        self.data = data
        self.index = -1
        self.last_key = max(data.keys(), default=-1)

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index > self.last_key:
            raise StopIteration
        return self.data.get(self.index, 0)


data1 = SparseList()
data1[0] = 1
data1[2] = 2

for iter1 in data1:
    for iter2 in data1:
        print(iter1, iter2)
