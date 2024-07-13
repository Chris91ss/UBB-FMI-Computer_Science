#pragma once

#include <iostream>
using namespace std;

class Person{
private:
    string name;
    string latitude;
    string longitude;
    string organiserStatus;

public:
    Person(string name, string latitude, string longitude, string organiserStatus);
    string getName();
    string getLatitude();
    string getLongitude();
    string getOrganiserStatus();
    void setName(string name);
    void setLatitude(string latitude);
    void setLongitude(string longitude);
    void setOrganiserStatus(string organiserStatus);
    string toString();
    friend ostream& operator<<(ostream& os, const Person& person);
    friend istream& operator>>(istream& is, Person& person);
    ~Person() = default;
};