#include "event.h"

Event::Event(string organiser, string name, string description, string latitude, string longitude, string date) {
    this->organiser = organiser;
    this->name = name;
    this->description = description;
    this->latitude = latitude;
    this->longitude = longitude;
    this->date = date;
}

string Event::getOrganiser() {
    return this->organiser;
}

string Event::getName() {
    return this->name;
}

string Event::getDescription() {
    return this->description;
}

string Event::getLatitude() {
    return this->latitude;
}

string Event::getLongitude() {
    return this->longitude;
}

string Event::getDate() {
    return this->date;
}

vector<string> Event::getAttendees() {
    return this->attendees;
}

void Event::setOrganiser(string organiser) {
    this->organiser = organiser;
}

void Event::setName(string name) {
    this->name = name;
}

void Event::setDescription(string description) {
    this->description = description;
}

void Event::setLatitude(string latitude) {
    this->latitude = latitude;
}

void Event::setLongitude(string longitude) {
    this->longitude = longitude;
}

void Event::setDate(string date) {
    this->date = date;
}

void Event::addAttendee(string attendee) {
    this->attendees.push_back(attendee);
}

string Event::toString() {
    return "Organiser: " + this->organiser + "Name: " + this->name + "Latitude: " + this->latitude + "Longitude: " + this->longitude + "Date: " + this->date;
}

ostream& operator<<(ostream& os, const Event& event) {
    os << event.organiser << ";" << event.name << ";" << event.description << ";" << event.latitude << ";" << event.longitude << ";" << event.date;
    for (const auto& attendee : event.attendees) {
        os << ";" << attendee;
    }
    return os;
}

istream& operator>>(istream& is, Event& event) {
    getline(is, event.organiser, ';');
    getline(is, event.name, ';');
    getline(is, event.description, ';');
    getline(is, event.latitude, ';');
    getline(is, event.longitude, ';');
    getline(is, event.date);

    string attendee;
    while (getline(is, attendee, ';')) {
        event.attendees.push_back(attendee);
    }
    return is;
}
