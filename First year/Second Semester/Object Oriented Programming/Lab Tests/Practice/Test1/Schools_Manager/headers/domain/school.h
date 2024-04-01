#pragma once
#include <string>
#include "location.h"
#include "dateTime.h"

using namespace std;

class School {
private:
    string name;
    Location location;
    DateTime dateOfVisit;
    bool wasVisited;
public:
    School();
    School(const string &name, const Location &location, const DateTime &dateOfVisit, bool wasVisited);
    School(const School &school);
    ~School();
    School &operator=(const School &school);
    bool operator==(const School &school);

    string getName() const;
    Location getLocation() const;
    DateTime getDateOfVisit() const;
    bool getWasVisited() const;

    void setName(const string &name);
    void setLocation(const Location &location);
    void setDateOfVisit(const DateTime &dateOfVisit);
    void setWasVisited(bool wasVisited);
};