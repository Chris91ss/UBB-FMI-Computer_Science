a = 1


def f(a):
    a = 2


def g(a):
    a[0] = 2


x = 3
f(x)
print(a)
print(x)
x = [3, 3]
g(x)
print(x)