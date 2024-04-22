#pragma once
#include "medicalAnalysis.h"

class BP: public MedicalAnalysis {
private:
    int systolicValue;
    int diastolicValue;
public:
    BP(const string &date, int systolicValue, int diastolicValue);
    bool isResultOK() const override;
    string toString() const override;
    ~BP() override = default;
};