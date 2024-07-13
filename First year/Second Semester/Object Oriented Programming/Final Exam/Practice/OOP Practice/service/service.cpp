#include "service.h"

Service::Service(Repository *repository) {
    this->repository = repository;
    this->repository->loadEventsFromFile("../data/events.txt");
    this->repository->loadPersonsFromFile("../data/persons.txt");
}

void Service::addEvent(string organiser, string name, string description, string latitude, string longitude, string date) {
    Event *event = new Event(organiser, name, description, latitude, longitude, date);
    for(auto & event : this->repository->getEvents())
    {
        if(event->getName() == name && event->getLatitude() == latitude && event->getLongitude() == longitude)
        {
            throw runtime_error("Event already exists!");
        }
    }
    this->repository->addEvent(event);
    notify();
}

void Service::addPerson(string name, string latitude, string longitude, string organiserStatus) {
    Person *person = new Person(name, latitude, longitude, organiserStatus);
    this->repository->addPerson(person);
    notify();
}

void Service::removeEvent(string name) {
    vector<Event*> events = this->repository->getEvents();
    for (int i = 0; i < events.size(); i++) {
        if (events[i]->getName() == name) {
            this->repository->removeEvent(events[i]);
            notify();
            return;
        }
    }
}

void Service::removePerson(string name) {
    vector<Person*> persons = this->repository->getPersons();
    for (int i = 0; i < persons.size(); i++) {
        if (persons[i]->getName() == name) {
            this->repository->removePerson(persons[i]);
            notify();
            return;
        }
    }
}

void Service::updateEvent(string name, string description, string latitude, string longitude, string date) {
    vector<Event*> events = this->repository->getEvents();
    for (int i = 0; i < events.size(); i++) {
        if (events[i]->getName() == name) {
            this->repository->updateEvent(events[i], name, description, latitude, longitude, date);
            notify();
            return;
        }
    }
}

void Service::updatePerson(string name, string latitude, string longitude, string organiserStatus) {
    vector<Person*> persons = this->repository->getPersons();
    for (int i = 0; i < persons.size(); i++) {
        if (persons[i]->getName() == name) {
            this->repository->updatePerson(persons[i], name, latitude, longitude, organiserStatus);
            notify();
            return;
        }
    }
}

void Service::saveEventsToFile(string filename) {
    this->repository->saveEventsToFile(filename);
}

void Service::savePersonsToFile(string filename) {
    this->repository->savePersonsToFile(filename);
}

vector<Event*> Service::getEvents() {
    return this->repository->getEvents();
}

vector<Person*> Service::getPersons() {
    return this->repository->getPersons();
}

vector<Event*> Service::getEventsByDate() {
    vector<Event*> events = this->repository->getEvents();
    sort(events.begin(), events.end(), [](Event *a, Event *b) {
        return a->getDate() < b->getDate();
    });
    return events;
}

bool Service::isPersonGoingToEvent(string personName, string eventName) {
    Event* event = this->getEventByName(eventName);
    if (!event) {
        return false;
    }
    vector<string> attendees = event->getAttendees();
    return find(attendees.begin(), attendees.end(), personName) != attendees.end();
}

Event* Service::getEventByName(string eventName) {
    vector<Event*> events = this->repository->getEvents();
    for (auto &event : events) {
        if (event->getName() == eventName) {
            return event;
        }
    }
    return nullptr;
}

void Service::markPersonAsGoingToEvent(string personName, string eventName) {
    Event* event = this->getEventByName(eventName);
    if (!event) {
        throw runtime_error("Event not found!");
    }
    if (this->isPersonGoingToEvent(personName, eventName)) {
        throw runtime_error("Person already marked as going!");
    }
    event->addAttendee(personName);
    this->repository->updateEvent(event, event->getName(), event->getDescription(), event->getLatitude(), event->getLongitude(), event->getDate());
}



