#include <cassert>
#include <iostream>
#include <string.h>
#include <vector>
#include <string>
using namespace std;

class Complex {
private:
    int real;
    int imaginary;

public:
    Complex(int real = 0, int imaginary = 0): real(real), imaginary(imaginary) {}

    int getReal() {
        return real;
    }

    int getImaginary() {
        return imaginary;
    }

    bool operator==(const Complex& other) const {
        return real == other.real && imaginary == other.imaginary;
    }

    Complex& operator/(int divisor) {
        if(divisor == 0) {
            throw runtime_error("Division by zero!");
        }
        real /= divisor;
        imaginary /= divisor;
        return *this;
    }

    friend ostream& operator<<(ostream &os, const Complex &c) {
        os << c.real << "+" << c.imaginary << "i";
        return os;
    }
};

template <typename T>
class Vector {
private:
    vector<T> v;
public:
    Vector(vector<T> v): v(v) {}
    void printAll(ostream &os) {
        for(auto& el : v) {
            os << el << ", ";
        }
    }
};

void complex() {
    Complex a{}, b{1, 2}, c{6, 4}, d{ b };
    assert(a.getReal() == 0 && a.getImaginary() == 0);
    assert(c.getImaginary() == 4);
    assert(b == d);
    Complex res1 = c / 2;
    cout << res1 << "\n"; // prints: 3+2i
    try {
        Complex res2 = b / 0;
    }
    catch (runtime_error& e) {
        assert(strcmp(e.what(), "Division by zero!") == 0);
    }

    Vector<string> v1{ std::vector<string>{"hello", "bye"} };
    v1.printAll(std::cout); // prints: hello, bye
    cout << endl;

    Vector<Complex> v2{ std::vector<Complex>{a, b, c, d} };
    v2.printAll(std::cout); // prints: 0+0i, 1+2i, 6+4i, 1+2i
    cout << endl;
}
//
// int main() {
//     complex();
//     return 0;
// }
