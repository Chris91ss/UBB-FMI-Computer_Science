#pragma once
#include <string>
#include <iostream>
using namespace std;


class User {
private:
    string name;
    string type;

public:
    User() = default;
    string getName();
    string getType();
    ~User() = default;
    friend ostream &operator<<(ostream &os, const User &user);
    friend istream &operator>>(istream &is, User &user);
    string toString() const;
};