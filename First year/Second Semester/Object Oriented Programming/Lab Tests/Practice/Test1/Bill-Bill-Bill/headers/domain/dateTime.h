#include <iostream>
using namespace std;

class DateTime {
public:
    DateTime();
    DateTime(int day, int month, int year);
    int day;
    int month;
    int year;
    DateTime &operator=(const DateTime &dateTime);
    friend ostream& operator<<(ostream& os, const DateTime& dateTime);
};