#pragma once
#include "appliance.h"

class Refrigerator : public Appliance {
private:
    string electricityUsageClass;
    bool hasFreezer;
public:
    Refrigerator(string id, string electricityUsageClass, bool hasFreezer);
    double consumedElectricity() const override;
    string toString() const override;
    ~Refrigerator() override = default;
};