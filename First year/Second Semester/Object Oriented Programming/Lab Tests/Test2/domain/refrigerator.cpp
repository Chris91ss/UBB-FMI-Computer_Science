
#include "refrigerator.h"

#include <utility>

Refrigerator::Refrigerator(string id, string electricityUsageClass, bool hasFreezer) {
    this->id = std::move(id);
    this->electricityUsageClass = std::move(electricityUsageClass);
    this->hasFreezer = hasFreezer;
}

double Refrigerator::consumedElectricity() const {
    int x = 0;
    double consumedEl;
    if(electricityUsageClass == "A")
        x = 3;
    else if(electricityUsageClass == "A++")
        x = 2;
    consumedEl = 30 * x;
    if(hasFreezer)
        consumedEl += 20;

    return consumedEl;
}

string Refrigerator::toString() const {
    return "Refrigerator " + id + " " + electricityUsageClass + " " + (hasFreezer ? "yes" : "no");
}
