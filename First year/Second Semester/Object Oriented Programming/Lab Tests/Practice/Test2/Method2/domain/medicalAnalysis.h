#pragma once
#include <string>
using namespace std;

class MedicalAnalysis
{
public:
    string date;
    virtual bool isResultOK() const = 0;
    virtual string toString() const = 0;
    virtual ~MedicalAnalysis() = default;
};