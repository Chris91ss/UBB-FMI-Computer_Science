#include "repository.h"

Repository::Repository() {
    this->events = vector<Event*>();
    this->persons = vector<Person*>();
}

void Repository::addEvent(Event* event) {
    this->events.push_back(event);
    this->saveEventsToFile("../data/events.txt");
}

void Repository::addPerson(Person* person) {
    this->persons.push_back(person);
    this->savePersonsToFile("../data/persons.txt");
}

void Repository::removeEvent(Event* event) {
    for (int i = 0; i < this->events.size(); i++) {
        if (this->events[i] == event) {
            this->events.erase(this->events.begin() + i);
            this->saveEventsToFile("../data/events.txt");
            return;
        }
    }
}

void Repository::removePerson(Person* person) {
    for (int i = 0; i < this->persons.size(); i++) {
        if (this->persons[i] == person) {
            this->persons.erase(this->persons.begin() + i);
            this->savePersonsToFile("../data/persons.txt");
            return;
        }
    }
}

void Repository::updateEvent(Event* event, string name, string description, string latitude, string longitude, string date) {
    for (int i = 0; i < this->events.size(); i++) {
        if (this->events[i] == event) {
            this->events[i]->setName(name);
            this->events[i]->setDescription(description);
            this->events[i]->setLatitude(latitude);
            this->events[i]->setLongitude(longitude);
            this->events[i]->setDate(date);
            this->saveEventsToFile("../data/events.txt");
            return;
        }
    }
}

void Repository::updatePerson(Person* person, string name, string latitude, string longitude, string organiserStatus) {
    for (int i = 0; i < this->persons.size(); i++) {
        if (this->persons[i] == person) {
            this->persons[i]->setName(name);
            this->persons[i]->setLatitude(latitude);
            this->persons[i]->setLongitude(longitude);
            this->persons[i]->setOrganiserStatus(organiserStatus);
            this->savePersonsToFile("../data/persons.txt");
            return;
        }
    }
}

void Repository::saveEventsToFile(string filename) {
    ofstream file(filename);
    for (const auto& event : this->events) {
        file << *event << endl;
    }
    file.close();
}

void Repository::savePersonsToFile(string filename) {
    ofstream file(filename);
    for (const auto& person : this->persons) {
        file << *person << endl;
    }
    file.close();
}

void Repository::loadEventsFromFile(string filename) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string organiser, name, description, latitude, longitude, date;
        getline(ss, organiser, ';');
        getline(ss, name, ';');
        getline(ss, description, ';');
        getline(ss, latitude, ';');
        getline(ss, longitude, ';');
        getline(ss, date);
        Event* event = new Event(organiser, name, description, latitude, longitude, date);
        this->events.push_back(event);
    }
    file.close();
}

void Repository::loadPersonsFromFile(string filename) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string name, latitude, longitude, organiserStatus;
        getline(ss, name, ';');
        getline(ss, latitude, ';');
        getline(ss, longitude, ';');
        getline(ss, organiserStatus);
        Person* person = new Person(name, latitude, longitude, organiserStatus);
        this->persons.push_back(person);
    }
    file.close();
}

vector<Event*> Repository::getEvents() {
    return this->events;
}

vector<Person*> Repository::getPersons() {
    return this->persons;
}

void Repository::markPersonAsGoingToEvent(Event* event, string personName) {
    event->addAttendee(personName);
    this->saveEventsToFile("../data/events.txt");
}
