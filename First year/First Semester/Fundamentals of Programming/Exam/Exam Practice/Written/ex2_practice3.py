class FibMatrix:
    def __init__(self, size):
        self.size = size
        self.offset = 0

        self.prev = 0
        self.current = 1
        self.curr_index = 0

    def __str__(self):
        if self.size < 1:
            return ""

        prev = 0
        current = 1
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                result += f"{prev + self.offset} "
                prev, current = current, prev + current
            result += "\n"

        return result.strip()

    def __add__(self, integer):
        self.offset += integer
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_index == self.size * self.size:
            self.curr_index = 0
            self.prev = 0
            self.current = 1
            raise StopIteration

        aux = self.prev
        self.prev, self.current = self.current, self.prev + self.current
        self.curr_index += 1

        return aux + self.offset


fm = FibMatrix(2)
print(fm)

fm = FibMatrix(3)
print(fm)

fm2 = fm + 10
print(fm2)

for i in fm2:
    print(i)


