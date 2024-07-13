#include <vector>
#include <string>
#include <cassert>
#include <stdexcept>
using namespace std;


template <typename T>
T fct(const vector<T>& v) {
    if (v.empty()) {
        throw std::runtime_error("Empty vector");
    }

    T max = v[0];
    for (size_t i = 1; i < v.size(); ++i) {
        if (v[i] > max) {
            max = v[i];
        }
    }

    return max;
}

void testFct() {
    vector<int> v1{ 4, 2, 1, 6, 3, -4 };
    assert(fct<int>(v1) == 6);

    vector<int> v2;
    try {
        fct<int>(v2);
        assert(false);
    } catch (std::exception&) {
        assert(true);
    }

    vector<double> v3{ 2, 10.5, 6.33, -100, 9, 1.212 };
    assert(fct<double>(v3) == 10.5);

    vector<string> v4{ "y", "q", "a", "m" };
    assert(fct<string>(v4) == "y");
}

// int main() {
//     testFct();
//     return 0;
// }