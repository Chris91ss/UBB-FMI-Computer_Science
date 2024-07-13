//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_CONTROLLER_H
#define VOLUNTEERING_CONTROLLER_H


#include "Subject.h"
#include "Repository.h"

class Controller : public Subject {

private:
    Repository &repository;

public:
    Controller(Repository &repository) : repository(repository) {};

    void addVolunteer(const std::string &name, const std::string &email, const std::vector<std::string> &interests);

    void assignVolunteer(const std::string &name, const std::string &email, Department *department);

    Department *getDepartment(int index);

    std::vector<Department> &getDepartments();

    std::vector<Volunteer> &getVolunteers();

};


#endif //VOLUNTEERING_CONTROLLER_H
