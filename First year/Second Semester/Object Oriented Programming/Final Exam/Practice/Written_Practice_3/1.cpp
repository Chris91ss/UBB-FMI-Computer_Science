#include <iostream>
#include <vector>
#include <string>
#include <cassert>
using namespace std;


template <typename T>
T fct(vector<T> vector) {
    if (vector.empty()) {
        throw std::exception();
    }
    T sum = vector[0];
    for (int i = 1; i < vector.size(); i++) {
        sum += vector[i];
    }
    return sum;
}


void testfct() {
    vector<int> v1{ 4, 2, 1, -4 };
    assert(fct<int>(v1) == 3);
    vector<int> v2;
    try {
        fct<int>(v2);
        assert(false);
    } catch (std::exception&) {
        assert(true);
    }

    vector<double> v3{ 2, 10.5, 5, -10 };
    assert(fct<double>(v3) == 7.5);

    vector<string> v4{ "y", "q", "a", "m" };
    assert(fct<string>(v4) == "yqam");
}
//
// int main() {
//     testfct();
//     return 0;
// }
