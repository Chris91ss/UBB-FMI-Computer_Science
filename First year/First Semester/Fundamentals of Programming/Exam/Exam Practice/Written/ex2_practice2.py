class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = {}

    def set(self, row, col, value):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Index out of range")
        if value != 0:
            self.matrix[(row, col)] = value

    def get(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Index out of range")
        return self.matrix.get((row, col), 0)

    def __str__(self):
        result = ""
        for i in range(self.rows):
            for j in range(self.cols):
                result += str(self.get(i, j)) + " "
            result += "\n"
        return result.strip()


m1 = SparseMatrix(3, 3)
m1.set(1, 1, 2)
m1.set(2, 2, 4)
print(m1)

try:
    m1.set(3, 3, 99)
except Exception as e:
    print(type(e))

m1.set(1, 1, m1.get(1, 1) + 1)
print(m1)
