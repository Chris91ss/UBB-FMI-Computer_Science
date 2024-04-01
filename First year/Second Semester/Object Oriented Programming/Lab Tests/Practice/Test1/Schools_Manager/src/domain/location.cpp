#include "location.h"

Location::Location() : longitude(0), latitude(0) {}

Location::Location(double longitude, double latitude) {
    this->longitude = longitude;
    this->latitude = latitude;
}

double Location::getLongitude() const {
    return this->longitude;
}

double Location::getLatitude() const {
    return this->latitude;
}

void Location::setLongitude(double newLongitude) {
    this->longitude = newLongitude;
}

void Location::setLatitude(double newLatitude) {
    this->latitude = newLatitude;
}

Location &Location::operator=(const Location &location) {
    this->latitude = location.latitude;
    this->longitude = location.longitude;
    return *this;
}
