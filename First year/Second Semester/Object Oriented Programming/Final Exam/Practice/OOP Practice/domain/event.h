#pragma once
#include <iostream>
#include <vector>
using namespace std;

class Event {
private:
    string organiser;
    string name;
    string description;
    string latitude;
    string longitude;
    string date;
    vector<string> attendees;

public:
    Event(string organiser, string name, string description, string latitude, string longitude, string date);
    string getOrganiser();
    string getName();
    string getDescription();
    string getLatitude();
    string getLongitude();
    string getDate();
    vector<string> getAttendees();
    void setOrganiser(string organiser);
    void setName(string name);
    void setDescription(string description);
    void setLatitude(string latitude);
    void setLongitude(string longitude);
    void setDate(string date);
    void addAttendee(string attendee);
    string toString();
    friend ostream& operator<<(ostream& os, const Event& event);
    friend istream& operator>>(istream& is, Event& event);
    ~Event() = default;
};

