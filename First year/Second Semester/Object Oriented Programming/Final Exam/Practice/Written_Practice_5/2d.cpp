#include <iostream>
using namespace std;

class A {
private:
    int* x;
public:
    static int noOfInstances;

    A(int _x = 5) {
        x = new int(_x);
        noOfInstances++;
    }

    int get() { return *x; }
    void set(int _x) { *x = _x; }
    ~A() { delete x; }
};

int A::noOfInstances = 0;

// 2 2 10 5 10
// int main() {
//     A a1, a2;
//     cout << A::noOfInstances << " ";
//     A a3 = a1;
//     cout << A::noOfInstances << " ";
//     a1.set(10);
//     cout << a1.get() << " ";
//     cout << a2.get() << " ";
//     cout << a3.get() << " ";
//     return 0;
// }
