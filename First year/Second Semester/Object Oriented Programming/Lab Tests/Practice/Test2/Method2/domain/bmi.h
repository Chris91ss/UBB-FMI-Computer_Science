#include "medicalAnalysis.h"

class BMI : public MedicalAnalysis {
private:
    double value;
public:
    BMI(const string &date, double value);
    bool isResultOK() const override;
    string toString() const override;
    ~BMI() override = default;
};