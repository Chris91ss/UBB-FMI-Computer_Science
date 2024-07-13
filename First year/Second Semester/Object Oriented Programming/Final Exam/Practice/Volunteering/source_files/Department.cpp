//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include "../header_files/Department.h"
#include "../header_files/utils.h"

using namespace std;

string Department::getName() const {
    return this->name;
}

string Department::getDescription() const {
    return this->description;
}

void Department::setName(const string &name) {
    this->name = name;
}

void Department::setDescription(const string &description) {
    this->description = description;
}

bool Department::operator==(const Department &other) const {
    return this->name == other.name;
}

bool Department::operator!=(const Department &other) const {
    return !(*this == other);
}

std::ostream &operator<<(ostream &os, const Department &department) {
    os << department.name << ";" << department.description;
    return os;
}

std::istream &operator>>(istream &is, Department &department) {
    string line;
    getline(is, line);

    vector<string> tokens = tokenize(line, ';');
    if (tokens.size() != 2) {
        return is;
    }

    department.setName(trim(tokens[0]));
    department.setDescription(trim(tokens[1]));

    return is;
}
