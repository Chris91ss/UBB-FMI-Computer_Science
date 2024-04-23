
#include "dishWasher.h"

DishWasher::DishWasher(string id, double consumedElectricityForOneHour) {
    this->id = std::move(id);
    this->consumedElectricityForOneHour = consumedElectricityForOneHour;
}

double DishWasher::consumedElectricity() const {
    return consumedElectricityForOneHour * 20;
}

string DishWasher::toString() const {
    return "DishWasher " + id + " " + to_string(consumedElectricityForOneHour);
}
