#pragma once
#include <iostream>
#include "../domain/event.h"
#include "../domain/person.h"
#include <vector>
#include <fstream>
#include <sstream>
using namespace std;

class Repository {
private:
    vector<Event*> events;
    vector<Person*> persons;
public:
    Repository();
    void addEvent(Event* event);
    void addPerson(Person* person);
    void removeEvent(Event* event);
    void removePerson(Person* person);
    void updateEvent(Event* event, string name, string description, string latitude, string longitude, string date);
    void updatePerson(Person* person, string name, string latitude, string longitude, string organiserStatus);
    void saveEventsToFile(string filename);
    void savePersonsToFile(string filename);
    void loadEventsFromFile(string filename);
    void loadPersonsFromFile(string filename);
    vector<Event*> getEvents();
    vector<Person*> getPersons();
    ~Repository() = default;
    void markPersonAsGoingToEvent(Event* event, string personName);
};

