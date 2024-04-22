#include "ui/ui.h"
#include "domain/bmi.h"
#include "domain/bp.h"

int main()
{
    Person person("Chris");

    MedicalAnalysis* analysis1 = new BMI("2021.03.01", 23.5);
    MedicalAnalysis* analysis2 = new BP("2021.03.02", 120, 80);

    person.addAnalysis(analysis1);
    person.addAnalysis(analysis2);

    UI ui(person);
    ui.run();

    return 0;
}