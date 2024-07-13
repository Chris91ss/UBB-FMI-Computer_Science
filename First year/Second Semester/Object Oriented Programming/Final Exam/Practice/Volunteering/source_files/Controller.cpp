//
// Created by qdeni on 6/25/2023.
//

#include <stdexcept>
#include "../header_files/Controller.h"

using namespace std;

void Controller::addVolunteer(const std::string &name, const std::string &email,
                              const std::vector<std::string> &interests) {
    if (name.empty() || email.empty()) {
        throw runtime_error("Invalid volunteer data!");
    }

    Volunteer volunteer(name, email, interests, "null");
    this->repository.addVolunteer(volunteer);
    this->notify();
}

void Controller::assignVolunteer(const std::string &name, const std::string &email, Department *department) {
    this->repository.assignVolunteer(name, email, department);
    this->notify();
}

Department *Controller::getDepartment(int index) {
    return this->repository.getDepartment(index);
}

vector<Department> &Controller::getDepartments() {
    return this->repository.getDepartments();
}

vector<Volunteer> &Controller::getVolunteers() {
    return this->repository.getVolunteers();
}
