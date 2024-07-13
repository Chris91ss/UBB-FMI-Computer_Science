#pragma once
#include <iostream>
#include <algorithm>
#include "../repository/repository.h"
#include "../subject.h"


class Service : public Subject{
private:
    Repository *repository;
public:
    Service(Repository *repository);
    void addEvent(string organiser, string name, string description, string latitude, string longitude, string date);
    void addPerson(string name, string latitude, string longitude, string organiserStatus);
    void removeEvent(string name);
    void removePerson(string name);
    void updateEvent(string name, string description, string latitude, string longitude, string date);
    void updatePerson(string name, string latitude, string longitude, string organiserStatus);
    void saveEventsToFile(string filename);
    void savePersonsToFile(string filename);
    vector<Event*> getEvents();
    vector<Person*> getPersons();
    ~Service() = default;
    vector<Event*> getEventsByDate();
    bool isPersonGoingToEvent(string personName, string eventName);
    Event* getEventByName(string eventName);
    void markPersonAsGoingToEvent(string personName, string eventName);
};