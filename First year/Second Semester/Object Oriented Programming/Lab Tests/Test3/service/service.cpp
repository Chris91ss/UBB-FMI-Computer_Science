#include "service.h"

Service::Service(Repository *repository) {
    this->repository = repository;
}

void Service::Add(Disorder *disorder) {
    this->repository->addDisorder(disorder);
}

vector<Disorder *> Service::GetDisorders() const {
    return this->repository->getDisorders();
}

vector<Disorder *> Service::GetSortedDisorders() const {
    return this->repository->getDisordersSorted();
}

void Service::readFromFile(const string &filename) {
    string line, category, name, symptomsString;
    vector<string> symptoms;

    ifstream file(filename);

    if(!file.is_open())
        throw runtime_error("File could not be opened!");

    while(getline(file, line)) {
        stringstream lineStream(line);

        getline(lineStream, category, '|');
        getline(lineStream, name, '|');
        getline(lineStream, symptomsString);

        stringstream symptomsStream(symptomsString);
        string symptom;
        while(getline(symptomsStream, symptom, ',')) {
            symptoms.push_back(symptom);
        }

        auto *disorder = new Disorder(category, name, symptoms);
        this->Add(disorder);
        symptoms.clear();
    }

    file.close();
}

vector<string> Service::GetDisorderSymptoms(const string &disorderName) const {
    for(auto &disorder : this->GetDisorders()) {
        if(disorder->getName() == disorderName)
            return disorder->getSymptoms();
    }
}

bool Service::searchDisorder(const string &disorderName) const {
    for(auto &disorder : this->GetDisorders()) {
        if(disorder->getName() == disorderName)
            return true;
    }

    return false;
}

