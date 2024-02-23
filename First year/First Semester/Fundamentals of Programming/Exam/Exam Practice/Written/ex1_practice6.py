class A:
    def __str__(self):
        return "a"


class B(A):
    def __init__(self, a=None):
        self._a = a

    def __str__(self):
        return str(self._a) + "b" + A.__str__(self)


a = A()
print(a)
b = B(a)
print(b)
c = B(b)
print(c)
