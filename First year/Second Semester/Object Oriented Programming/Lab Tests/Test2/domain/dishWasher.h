#pragma once

#include "appliance.h"

class DishWasher : public Appliance {
private:
    double consumedElectricityForOneHour;
public:
    DishWasher(string id, double consumedElectricityForOneHour);
    double consumedElectricity() const override;
    string toString() const override;
    ~DishWasher() override = default;
};