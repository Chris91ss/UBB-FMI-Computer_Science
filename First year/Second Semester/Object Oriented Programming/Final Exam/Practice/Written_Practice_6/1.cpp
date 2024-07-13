#include <iostream>
#include <cassert>
#include <vector>
#include <memory>
#include <string>
using namespace std;

class Object {
public:
    virtual void print() = 0;
    virtual ~Object() {}
};

class Integer : public Object {
private:
    int value;
public:
    Integer(int v) : value(v) {}
    void print() override {
        cout << value << " ";
    }
};

class String : public Object {
private:
    string str;
public:
    String(string s) : str(s) {}

    bool operator==(const string& s) {
        return str == s;
    }

    void print() override {
        cout << str << " ";
    }
};

class MyObjectList {
private:
    vector<unique_ptr<Object>> list;
public:
    MyObjectList& add(Object* o) {
        list.emplace_back(o);
        return *this;
    }

    size_t length() const {
        return list.size();
    }

    typename vector<unique_ptr<Object>>::iterator begin() {
        return list.begin();
    }

    typename vector<unique_ptr<Object>>::iterator end() {
        return list.end();
    }
};

void function() {
    MyObjectList list;
    list.add(new Integer(2)).add(new String("Hi"));
    String* s = new String("Bye");
    assert(*s == "Bye");
    list.add(s).add(new Integer(5)); // IMPLEMENT THIS OPERATION
    assert(list.length() == 4);

    // prints: 2 Hi Bye 5
    for (const auto& o : list)
        o->print();
    cout << endl;
}

// int main() {
//     function();
//     return 0;
// }
