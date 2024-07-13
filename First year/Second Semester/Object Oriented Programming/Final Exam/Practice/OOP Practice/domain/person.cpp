#include "person.h"

Person::Person(string name, string latitude, string longitude, string organiserStatus) {
    this->name = name;
    this->latitude = latitude;
    this->longitude = longitude;
    this->organiserStatus = organiserStatus;
}

string Person::getName() {
    return this->name;
}

string Person::getLatitude() {
    return this->latitude;
}

string Person::getLongitude() {
    return this->longitude;
}

string Person::getOrganiserStatus() {
    return this->organiserStatus;
}

void Person::setName(string name) {
    this->name = name;
}

void Person::setLatitude(string latitude) {
    this->latitude = latitude;
}

void Person::setLongitude(string longitude) {
    this->longitude = longitude;
}

void Person::setOrganiserStatus(string organiserStatus) {
    this->organiserStatus = organiserStatus;
}

string Person::toString() {
    return this->name + " " + this->latitude + " " + this->longitude + " " + this->organiserStatus;
}

ostream& operator<<(ostream& os, const Person& person) {
    os << person.name << ";" << person.latitude << ";" << person.longitude << ";" << person.organiserStatus;
    return os;
}

istream& operator>>(istream& is, Person& person) {
    getline(is, person.name, ';');
    getline(is, person.latitude, ';');
    getline(is, person.longitude, ';');
    getline(is, person.organiserStatus);
    return is;
}

