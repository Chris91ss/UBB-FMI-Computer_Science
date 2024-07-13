#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

template <typename T>
class SmartPointer {
private:
    T* p;
public:
    SmartPointer(T* ptr) : p(ptr) {}

    T& operator*() {
        return *p;
    }

    bool operator==(const SmartPointer& other) const {
        return *p == *other.p;
    }
};

template <typename T>
class Vector {
private:
    vector<T> v;
public:
    Vector& add(T e) {
        v.push_back(e);
        return *this;
    }

    Vector& operator-(T e) {
        auto it = find(v.begin(), v.end(), e);
        if (it == v.end())
            throw runtime_error("Element does not exist");
        v.erase(it);
        return *this;
    }

    Vector& operator=(const Vector<T>& other) {
        if (this != &other) {
            v = other.v;
        }
        return *this;
    }

    typename vector<T>::iterator begin() {
        return v.begin();
    }

    typename vector<T>::iterator end() {
        return v.end();
    }
};

void functionVs() {
    SmartPointer<int> i1(new int(1));
    SmartPointer<int> i2(new int(2));
    SmartPointer<int> i3(new int(3));
    Vector<SmartPointer<int>> v1{};
    v1.add(i1).add(i2).add(i3);
    for (auto e : v1)
        cout << *e << " "; // prints 1, 2, 3
    cout << endl;

    SmartPointer<string> s1(new string("A"));
    SmartPointer<string> s2 = s1;
    SmartPointer<string> s3(new string("C"));
    Vector<SmartPointer<string>> v2{};
    v2.add(s2).add(s3);
    try {
        v2 = v2 - s2;   // IMPLEMENT THIS OPERATION
        v2 = v2 - s3;   // IMPLEMENT THIS OPERATION
    }
    catch (std::runtime_error& ex) {
        cout << ex.what(); // prints: "Element does not exist"
    }

    // memory is correctly deallocated
}
//
// int main() {
//     functionVs();
//     return 0;
// }
