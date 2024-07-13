//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_REPOSITORY_H
#define VOLUNTEERING_REPOSITORY_H

#include "Volunteer.h"

class Repository {

private:
    std::vector<Department> departments;
    std::vector<Volunteer> volunteers;
    std::string departmentsFile;
    std::string volunteersFile;

public:
    Repository(const std::string &departmentsFile, const std::string &volunteersFile);

    void addVolunteer(const Volunteer &volunteer);

    void assignVolunteer(const std::string &name, const std::string &email, Department *department);

    Department *getDepartment(int index);

    std::vector<Department> &getDepartments();

    std::vector<Volunteer> &getVolunteers();

private:
    void linkVolunteersToDepartments();

    void loadDepartments();

    void loadVolunteers();

    void saveDepartments();

    void saveVolunteers();

};


#endif //VOLUNTEERING_REPOSITORY_H
