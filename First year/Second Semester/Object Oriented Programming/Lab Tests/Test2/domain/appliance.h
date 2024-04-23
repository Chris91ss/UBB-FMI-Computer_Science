#pragma once
#include <string>
using namespace std;

class Appliance {
protected:
    string id;
public:
    virtual double consumedElectricity() const = 0;
    virtual string toString() const = 0;
    virtual string getId() const { return id; }
    virtual ~Appliance() = default;
};