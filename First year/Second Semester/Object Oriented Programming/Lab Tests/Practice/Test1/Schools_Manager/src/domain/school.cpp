
#include "school.h"

School::School() : name(""), location(Location()), dateOfVisit(DateTime()), wasVisited(false) {}


School::School(const string &name, const Location &location, const DateTime &dateOfVisit, bool wasVisited) {
    this->name = name;
    this->location = location;
    this->dateOfVisit = dateOfVisit;
    this->wasVisited = wasVisited;
}

School::School(const School &school) {
    this->name = school.name;
    this->location = school.location;
    this->dateOfVisit = school.dateOfVisit;
    this->wasVisited = school.wasVisited;
}

School::~School() = default;

School &School::operator=(const School &school) {
    this->name = school.name;
    this->location = school.location;
    this->dateOfVisit = school.dateOfVisit;
    this->wasVisited = school.wasVisited;
    return *this;
}

bool School::operator==(const School &school) {
    return this->name == school.name;
}

string School::getName() const {
    return this->name;
}

Location School::getLocation() const {
    return this->location;
}

DateTime School::getDateOfVisit() const {
    return this->dateOfVisit;
}

bool School::getWasVisited() const {
    return this->wasVisited;
}

void School::setName(const string &name) {
    this->name = name;
}

void School::setLocation(const Location &location) {
    this->location = location;
}

void School::setDateOfVisit(const DateTime &dateOfVisit) {
    this->dateOfVisit = dateOfVisit;
}

void School::setWasVisited(bool wasVisited) {
    this->wasVisited = wasVisited;
}
