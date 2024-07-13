//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include "../header_files/Programmer.h"
#include "../header_files/utils.h"

using namespace std;

string Programmer::getName() const {
    return name;
}

int Programmer::getId() const {
    return id;
}

void Programmer::setName(const string &name) {
    this->name = name;
}

void Programmer::setId(int id) {
    this->id = id;
}

bool Programmer::operator==(const Programmer &other) const {
    return this->name == other.name && this->id == other.id;
}

bool Programmer::operator!=(const Programmer &other) const {
    return !(*this == other);
}

std::ostream &operator<<(std::ostream &os, const Programmer &programmer) {
    os << programmer.name << "," << programmer.id;
    return os;
}

std::istream &operator>>(istream &is, Programmer &programmer) {
    string line;
    getline(is, line);

    vector<string> tokens = tokenize(line, ',');
    if (tokens.size() != 2) {
        return is;
    }

    programmer.setName(tokens[0]);
    try {
        programmer.setId(stoi(tokens[1]));
    } catch (exception &e) {
        return is;
    }

    return is;
}
