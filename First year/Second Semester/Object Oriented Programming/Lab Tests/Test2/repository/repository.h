#include "../domain/appliance.h"
#include <vector>
#include <fstream>

class Repository {
private:
    vector<Appliance*> appliances;
public:
    Repository();
    void addAppliance(Appliance* appliance);
    vector<Appliance*> getAllAppliances() const;
    vector<Appliance*> getAllWithConsumedElectricityLessThan(double maxConsumedElectricity) const;
    vector<Appliance*> getAllWithConsumedElectricityMoreThan(double maxConsumedElectricity) const;
    void writeToFile(const string& fileName, const double consumedElectricity) const;
    ~Repository();
};