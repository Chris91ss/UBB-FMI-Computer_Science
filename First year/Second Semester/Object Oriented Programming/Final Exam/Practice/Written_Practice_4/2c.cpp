#include <iostream>
#include <string>
using namespace std;

template <typename T>
class elem {
private:
    T x;
public:
    elem(T _x) : x(_x) {}
    static T add(T a, T b) { return a + b; }

    elem& operator+=(const T& a) {
        x += a;
        return *this;
    }

    T get() { return x; }
};

// Answer to life
// 42
// int main() {
//     cout << elem<string>::add("Answer to ", "life ") << endl;
//     elem<int> e(3);
//     e += 39;
//     cout << e.get();
//     return 0;
// }
