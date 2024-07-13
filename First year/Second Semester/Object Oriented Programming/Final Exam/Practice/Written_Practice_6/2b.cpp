#include <iostream>
#include <string>
using namespace std;

class Exception1 {
public:
    Exception1() { cout << "Exception1 "; }
    virtual void fct() { cout << "Ex1 "; }
    virtual ~Exception1() { cout << "~Exception1 "; }
};

class Exception2 : public Exception1 {
public:
    void fct() override { cout << "Ex2 "; }
    virtual ~Exception2() { cout << "~Exception2 "; }
};

string f(int x) {
    cout << "Hi ";
    if (x % 2 == 0)
        throw Exception1();
    else
        throw Exception2();
    return string("Bye ");
}

/// Hi Exception1 Ex2 ~Exception2 ~Exception1
// int main() {
//     try {
//         cout << f(5);
//         cout << f(2);
//     } catch (Exception1& ex) {
//         ex.fct();
//     } catch (Exception2& ex2) {
//         ex2.fct();
//     }
//     return 0;
// }
