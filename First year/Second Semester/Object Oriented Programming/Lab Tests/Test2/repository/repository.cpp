
#include "repository.h"

Repository::Repository() = default;

void Repository::addAppliance(Appliance *appliance) {
    appliances.push_back(appliance);
}

vector<Appliance *> Repository::getAllAppliances() const {
    return appliances;
}

vector<Appliance *> Repository::getAllWithConsumedElectricityLessThan(double maxConsumedElectricity) const {
    vector<Appliance*> filteredAppliances;
    for (auto appliance : appliances) {
        if (appliance->consumedElectricity() < maxConsumedElectricity) {
            filteredAppliances.push_back(appliance);
        }
    }

    return filteredAppliances;
}

vector<Appliance *> Repository::getAllWithConsumedElectricityMoreThan(double maxConsumedElectricity) const {
    vector<Appliance*> filteredAppliances;
    for (auto appliance : appliances) {
        if (appliance->consumedElectricity() > maxConsumedElectricity) {
            filteredAppliances.push_back(appliance);
        }
    }

    return filteredAppliances;
}

void Repository::writeToFile(const string& fileName, const double consumedElectricity) const {
    ofstream file(fileName);
    vector<Appliance*> sortedAppliances = getAllWithConsumedElectricityLessThan(consumedElectricity);
    for(int i = 0; i < sortedAppliances.size(); i++)
    {
        for(int j = i + 1; j < sortedAppliances.size(); j++)
        {
            if(sortedAppliances[i]->getId() > sortedAppliances[j]->getId())
            {
                Appliance* aux = sortedAppliances[i];
                sortedAppliances[i] = sortedAppliances[j];
                sortedAppliances[j] = aux;
            }
        }
    }
    for (auto appliance : sortedAppliances) {
        file << appliance->toString() << endl;
    }
    file.close();
}

Repository::~Repository() {
    for (auto appliance : appliances) {
        delete appliance;
    }
}
