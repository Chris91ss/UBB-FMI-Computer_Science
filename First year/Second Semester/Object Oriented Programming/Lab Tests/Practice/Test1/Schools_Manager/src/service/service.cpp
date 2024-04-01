
#include "service/service.h"

Service::Service(Repository <School> &repository) {
    this->repository = repository;
}

Service::Service(const Service &other) {
    this->repository = other.repository;
}

Service::~Service() = default;

void Service::addSchool(const School &school) {
    if(this->repository.searchElement(school))
        throw runtime_error("School already exists!");
    this->repository.addElement(school);
}

void Service::removeSchool(const string &name) {
    for(int i = 0; i < this->repository.getSize(); i++) {
        if(this->repository[i].getName() == name) {
            this->repository.removeElement(i);
            return;
        }
    }
    throw runtime_error("School does not exist!");
}

void Service::Generate5Schools() {
    this->addSchool(School("Avram_Iancu", Location(46.77, 23.60),
                           DateTime(15, 4, 2022), true));
    this->addSchool(School("George_Cosbuc", Location(46.77, 23.58),
                           DateTime(18, 4, 2022), false));
    this->addSchool(School("Alexandru_Vaida_Voieod", Location(46.77, 23.63),
                           DateTime(23, 4, 2022), false));
    this->addSchool(School("Romulus_Guga", Location(46.53, 24.57),
                           DateTime(4, 5, 2022), false));
}

DynamicVector<School> Service::getAllSchools() const {
    return this->repository.getAllElements();
}

DynamicVector<School> Service::getAllSchoolsSortedByName() const {
    DynamicVector<School> schools = this->repository.getAllElements();
    for(int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        for(int j = i + 1; j < schools.GetSizeOfDynamicVector(); j++) {
            if(schools[i].getName() > schools[j].getName()) {
                School aux = schools[i];
                schools[i] = schools[j];
                schools[j] = aux;
            }
        }
    }

    return schools;
}

DynamicVector<School> Service::getAllSchoolsAfterAGivenDate(const DateTime &date) {
    DynamicVector<School> schools = this->repository.getAllElements();
    DynamicVector<School> result;
    for(int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        if(schools[i].getDateOfVisit().getDay() < date.getDay() ||
           schools[i].getDateOfVisit().getMonth() < date.getMonth() ||
           schools[i].getDateOfVisit().getYear() < date.getYear())
            updateVisitedBool(i);
    }

    for(int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        if(schools[i].getDateOfVisit().getDay() >= date.getDay() ||
           schools[i].getDateOfVisit().getMonth() >= date.getMonth() ||
           schools[i].getDateOfVisit().getYear() >= date.getYear())
            if(!schools[i].getWasVisited())
                result.AddToDynamicVector(schools[i]);
    }

    return result;
}

void Service::updateVisitedBool(int index){
    this->repository[index].setWasVisited(true);
}
