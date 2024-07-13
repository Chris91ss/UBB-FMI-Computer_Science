#include "user.h"

string User::getName() {
    return name;
}

string User::getType() {
    return type;
}

string User::toString() const {
    return name + ";" + type;
}

ostream & operator<<(ostream &os, const User &user) {
    os << user.name << ";" << user.type;
    return os;
}

istream & operator>>(istream &is, User &user) {
    getline(is, user.name, ';');
    getline(is, user.type);
    return is;
}