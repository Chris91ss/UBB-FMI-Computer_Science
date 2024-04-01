#pragma once

class Location {
private:
    double longitude;
    double latitude;
public:
    Location();
    Location(double longitude, double latitude);
    double getLongitude() const;
    double getLatitude() const;
    void setLongitude(double newLongitude);
    void setLatitude(double newLatitude);
    Location &operator=(const Location &location);
};