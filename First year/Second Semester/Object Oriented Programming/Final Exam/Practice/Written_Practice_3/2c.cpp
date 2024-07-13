#include <iostream>
#include <string>

using namespace std;

template <typename T, typename U>
U fct2(T a, T b, U x, U y) {
    cout << a << " ";
    cout << b << " ";
    if (a == b)
        return x + y;
    return x;
}

class A {
    int a;
public:
    A(int _a) : a(_a) {}
    friend ostream& operator<<(ostream& os, const A& a) {
        os << a.a;
        return os;
    }
    A operator+(const A& a) const {
        return A(this->a + a.a);
    }
};

// 10 10 10 10 10.5 5 -2 -2 Goodluck! 1 1 5
// int main() {
//     cout << fct2<int, int>(10, 10, 5, 5) << " ";
//     cout << fct2<double, int>(10, 10.5, 5, 5) << " ";
//     cout << fct2<int, string>(-2, -2, "Good", "luck!") << " ";
//     cout << fct2<int, A>(1, 1, A(2), A(3));
//     return 0;
// }