#include <iostream>
#include <string>
#include <cassert>
#include <map>
#include <string.h>
using namespace std;

class Person {
private:
    int age;
    string name;
public:
    Person(const int &age, const string &name) : age(age), name(name) {}

    friend ostream& operator<<(ostream &os, const Person &p) {
        os << p.name << " is " << p.age << " years old";
        return os;
    }

    bool operator==(const Person& other) const {
        return age == other.age && name == other.name;
    }
};

template <typename T1, typename T2>
class MultiDictionary {
private:
    multimap<T1, T2> dict;
public:
    MultiDictionary& add(T1 key, T2 value) {
        dict.insert({key, value});
        return *this;
    }

    void print(ostream& os) const {
        for (auto& p : dict) {
            os << p.first << " " << p.second << "; ";
        }
        os << endl;
    }

    void erase(T1 key, T2 value) {
        auto range = dict.equal_range(key);
        for (auto it = range.first; it != range.second; ++it) {
            if (it->second == value) {
                dict.erase(it);
                return;
            }
        }
        if (range.first == range.second) {
            throw runtime_error("Key does not exist!");
        }
        throw runtime_error("Given value does not exist for given key!");
    }

    int sizeForKey(T1 key) const {
        return dict.count(key);
    }
};

void function123()
{
    MultiDictionary<int, string> d1{};
    d1.add(1, "a").add(2, "b").add(1, "c").add(3, "d");
    d1.print(std::cout); // prints 1 a; 1 c; 2 b; 3 d
    try {
        d1.erase(4, "w"); assert(false);
    }
    catch (std::runtime_error& e) {
        try {
            assert(strcmp(e.what(), "Key does not exist!") == 0);
            d1.erase(2, "w"); assert(false);
        }
        catch (std::runtime_error& e) {
            assert(strcmp(e.what(), "Given value does not exist for given key!") == 0);
        }
    }

    d1.erase(1, "a"); d1.print(std::cout); // prints 1 c; 2 b; 3 d
    MultiDictionary<string, Person> d2{};
    Person p1{ 23, "Mircea" }; Person p2{ 20, "Ioana" };
    std::cout << p2 << endl; // prints: Ioana is 20 years old
    d2.add("a", p1).add("a", p2);
    d2.print(std::cout); // prints: a Mircea is 23 years old; a Ioana is 20 years old
    assert(d2.sizeForKey("a") == 2); assert(d2.sizeForKey("b") == 0);
}

// int main()
// {
//     function123();
//     return 0;
// }
