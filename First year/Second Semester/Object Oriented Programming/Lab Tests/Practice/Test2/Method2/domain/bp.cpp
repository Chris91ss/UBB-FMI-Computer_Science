#include "bp.h"

BP::BP(const string &date, int systolicValue, int diastolicValue) : systolicValue(systolicValue), diastolicValue(diastolicValue) {
    this->date = date;
}

bool BP::isResultOK() const {
    return systolicValue >= 90 && systolicValue <= 119 &&
           diastolicValue >= 60 && diastolicValue <= 79;
}

string BP::toString() const {
    return "BP analysis on " + date + ": systolic = " + to_string(systolicValue) +
           ", diastolic = " + to_string(diastolicValue) +
           ", result is " + (isResultOK() ? "OK" : "Not OK");
}
