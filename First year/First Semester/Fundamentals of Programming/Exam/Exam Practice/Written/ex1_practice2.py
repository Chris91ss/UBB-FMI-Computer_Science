class X:
    def f(self):
        print("X")


class Y(X):
    def __init__(self, a):
        self._a = a

    def f(self):
        print("Y")
        self._a.f()


class Z(Y):
    def __init__(self, a):
        super().__init__(a)


for o in [Y(Y(X())), Z(Y(X()))]:
    o.f()
