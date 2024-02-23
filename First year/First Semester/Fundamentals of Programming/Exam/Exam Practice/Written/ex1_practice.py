def f(a, b):
    b.append(a)
    a = [a]
    b = b + a
    return b


x = 1
y = [2]
z = f(x, y)
print([1] == x)
print(id(y) == id(z))
print(y == z[0:2])
