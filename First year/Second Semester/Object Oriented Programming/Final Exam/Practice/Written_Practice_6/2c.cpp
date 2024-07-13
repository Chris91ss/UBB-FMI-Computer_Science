#include <iostream>
using namespace std;

class A {
private:
    int x;
public:
    A(int _x = 0) : x(_x) {}
    int get() const { return x; }
    friend class B;
};

class B {
private:
    A a;
public:
    B(const A& _a) : a(_a) {}
    B& operator+(const A& _a) {
        a.x += _a.x;
        return *this;
    }
    int get() { return a.x; }
};

/// 1 2 4 4
// int main() {
//     A a1(1), a2(2);
//     cout << a1.get() << " " << a2.get() << " ";
//
//     B b1(a1);
//     B b2 = b1 + a2 + a1;
//     cout << b1.get() << " " << b2.get() << " ";
//
//     return 0;
// }
