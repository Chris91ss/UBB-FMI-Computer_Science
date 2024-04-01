#pragma once
#include <iostream>
using namespace std;

class DateTime {
private:
    int day;
    int month;
    int year;
public:
    DateTime();
    DateTime(int day, int month, int year);
    int getDay() const;
    int getMonth() const;
    int getYear() const;
    void setDay(int newDay);
    void setMonth(int newMonth);
    void setYear(int newYear);
    DateTime &operator=(const DateTime &dateTime);
    friend ostream& operator<<(ostream& os, const DateTime& dateTime);
};