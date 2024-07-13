#include <iostream>
#include <vector>
using namespace std;

template <typename T>
class Adder {
private:
    vector<T> values;
    T currentSum;
public:
    Adder(T value): currentSum(value) {
        values.push_back(value);
    }
    Adder& operator+(T v) {
        values.push_back(v);
        currentSum += v;
        return *this;
    }
    Adder& operator++() {
        int last_value = values.back();
        values.push_back(last_value);
        currentSum += last_value;
        return *this;
    }

    Adder& operator--() {
        if(values.size() == 0)
            throw runtime_error("No more values!");
        currentSum -= values.back();
        values.pop_back();
        return *this;
    }

    T sum() {
        return currentSum;
    }
};


void function2() {
    Adder<int> add{5};
    add = add + 5 + 2;
    ++add;
    add + 8;
    cout << add.sum() << "\n";
    --add;
    cout << add.sum() << "\n";
    --(--add);
    cout << add.sum() << "\n";
    try {
        --(--(--add));
    }
    catch (runtime_error& ex) {
        std::cout << ex.what();
    }
}

// int main() {
//     function2();
//     return 0;
// }
