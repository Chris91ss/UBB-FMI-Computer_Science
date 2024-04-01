
#include "dateTime.h"

DateTime::DateTime() : day(0), month(0), year(0) {}

DateTime::DateTime(int day, int month, int year) {
    this->day = day;
    this->month = month;
    this->year = year;
}

int DateTime::getDay() const {
    return this->day;
}

int DateTime::getMonth() const {
    return this->month;
}

int DateTime::getYear() const {
    return this->year;
}

void DateTime::setDay(int newDay) {
    this->day = newDay;
}

void DateTime::setMonth(int newMonth) {
    this->month = newMonth;
}

void DateTime::setYear(int newYear) {
    this->year = newYear;
}

DateTime &DateTime::operator=(const DateTime &dateTime) {
    this->day = dateTime.day;
    this->month = dateTime.month;
    this->year = dateTime.year;
    return *this;
}

ostream &operator<<(ostream &os, const DateTime &dateTime) {
    if(dateTime.day < 10)
        os << "0" << dateTime.day << ".";
    else
        os << dateTime.day << ".";
    if(dateTime.month < 10)
        os << "0" << dateTime.month << ".";
    else
        os << dateTime.month << ".";
    os << dateTime.year;
    return os;
}
