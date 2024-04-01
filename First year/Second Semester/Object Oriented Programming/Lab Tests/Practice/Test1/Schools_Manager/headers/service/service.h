#pragma once
#include "school.h"
#include "repository/repository.h"

class Service{
private:
    Repository<School> repository;
public:
    Service(Repository<School> &repository);
    Service(const Service &other);
    ~Service();

    void addSchool(const School &school);
    void removeSchool(const string& name);
    void Generate5Schools();
    DynamicVector<School> getAllSchools() const;
    DynamicVector<School> getAllSchoolsSortedByName() const;
    DynamicVector<School> getAllSchoolsAfterAGivenDate(const DateTime &date);
    void updateVisitedBool(int index);
};