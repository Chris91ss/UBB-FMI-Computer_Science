
#include "bmi.h"

BMI::BMI(const string &date, double value) : value(value) {
    this->date = date;
}

bool BMI::isResultOK() const {
    return value >= 18.5 && value <= 25;
}

string BMI::toString() const {
    return "BMI analysis on " + date + ": value = " + to_string(value) +
           ", result is " + (isResultOK() ? "OK" : "Not OK");
}


