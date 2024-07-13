#include <iostream>
#include <set>
#include <string>
using namespace std;


template <typename T>
class SmartPointer {
private:
    T *p;
public:
    SmartPointer(T *p) : p(p) {}
    SmartPointer(const SmartPointer &other) : p(new T(*other.p)) {}
    ~SmartPointer() {
        delete p;
    }

    T& operator*() {
        return *p;
    }

    bool operator<(const SmartPointer& other) const {
        return *p < *other.p;
    }
};

template <typename T>
class Set {
private:
    set<T> elem;

public:
    Set& operator+(const T& element) {
        if (elem.find(element) != elem.end()) {
            throw runtime_error("Element already exists!");
        }
        elem.insert(element);
        return *this;
    }

    void remove(const T& element) {
        elem.erase(element);
    }

    typename set<T>::iterator begin() {
        return elem.begin();
    }

    typename set<T>::iterator end() {
        return elem.end();
    }

};

void function2() {
    SmartPointer<string> s1( new string("A") );
    SmartPointer<string> s2 = s1;
    SmartPointer<string> s3( new string("C") );
    Set<SmartPointer<string>> set1;

    try {
        set1 = set1 + s1; // IMPLEMENT THIS OPERATION
        set1 = set1 + s2; // IMPLEMENT THIS OPERATION
    }
    catch (std::runtime_error& ex) {
        cout << ex.what(); // prints: "Element already exists!"
    }

    SmartPointer<int> i1( new int(1) );
    SmartPointer<int> i2( new int(2) );
    SmartPointer<int> i3( new int(3) );
    Set<SmartPointer<int>> set2;
    set2 = set2 + i1; // IMPLEMENT THIS OPERATION
    set2 = set2 + i2; // IMPLEMENT THIS OPERATION
    set2 = set2 + i3; // IMPLEMENT THIS OPERATION
    set2.remove(i3);  // IMPLEMENT THIS OPERATION
    for (auto e : set2) {
        cout << *e << " "; // prints 2,
    }
    // memory is correctly deallocated
}
//
// int main() {
//     function2();
//     return 0;
// }