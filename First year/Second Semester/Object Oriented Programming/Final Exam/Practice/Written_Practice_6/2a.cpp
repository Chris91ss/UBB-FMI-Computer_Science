#include <iostream>
using namespace std;

class Base {
private:
    virtual void f() {
        std::cout << "Base" << "\n";
    }
public:
    virtual ~Base() {
        f();
    }
    void g() {
        f();
    }
};

class Derived : public Base {
private:
    void f() override {
        std::cout << "Derived" << "\n";
    }
public:
    void h() {
        Base::g();
        cout << "Function h" << "\n";
    }
    ~Derived() {
        f();
    }
};

// Derived Derived Function h Derived Base
// int main() {
//     Base* b = new Derived();
//     b->g();
//     Derived* d = dynamic_cast<Derived*>(b);
//     if (d != nullptr) {
//         d->h();
//     }
//     delete b;
//     return 0;
// }
