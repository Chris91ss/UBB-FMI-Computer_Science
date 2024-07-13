//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include "../header_files/Volunteer.h"
#include "../header_files/utils.h"

using namespace std;

string Volunteer::getName() const {
    return this->name;
}

string Volunteer::getEmail() const {
    return this->email;
}

vector<string> Volunteer::getInterests() const {
    return this->interests;
}

string Volunteer::getDepartmentName() const {
    return this->departmentName;
}

Department *Volunteer::getDepartment() const {
    return this->department;
}

void Volunteer::setName(const string &name) {
    this->name = name;
}

void Volunteer::setEmail(const string &email) {
    this->email = email;
}

void Volunteer::setInterests(const vector<string> &interests) {
    this->interests = interests;
}

void Volunteer::setDepartmentName(const string &departmentName) {
    this->departmentName = departmentName;
}

void Volunteer::setDepartment(Department *department) {
    this->department = department;
}

bool Volunteer::operator==(const Volunteer &other) const {
    return this->name == other.name && this->email == other.email;
}

bool Volunteer::operator!=(const Volunteer &other) const {
    return !(*this == other);
}

std::ostream &operator<<(ostream &os, const Volunteer &volunteer) {
    os << volunteer.name << ";" << volunteer.email << ";";
    for (auto it = volunteer.interests.begin(); it != volunteer.interests.end(); ++it) {
        os << *it;
        if (it != volunteer.interests.end() - 1) {
            os << "|";
        } else {
            os << ";";
        }
    }
    os << volunteer.departmentName;

    return os;
}

std::istream &operator>>(istream &is, Volunteer &volunteer) {
    string line;
    getline(is, line);

    vector<string> tokens = tokenize(line, ';');
    if (tokens.size() != 4) {
        return is;
    }

    volunteer.setName(trim(tokens[0]));
    volunteer.setEmail(trim(tokens[1]));
    volunteer.setInterests(tokenize(trim(tokens[2]), '|'));
    volunteer.setDepartmentName(trim(tokens[3]));
    volunteer.setDepartment(nullptr);

    return is;
}

string Volunteer::toString() const {
    string volunteerString = this->name + ", " + this->email + ", (";
    for (auto it = this->interests.begin(); it != this->interests.end(); ++it) {
        volunteerString += *it;
        if (it != this->interests.end() - 1) {
            volunteerString += "; ";
        }
    }
    volunteerString += ")";
    return volunteerString;
}
