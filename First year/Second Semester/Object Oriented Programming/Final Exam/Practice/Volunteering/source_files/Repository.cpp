//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include <stdexcept>
#include "../header_files/Repository.h"

using namespace std;

Repository::Repository(const std::string &departmentsFile, const std::string &volunteersFile) {
    this->departmentsFile = departmentsFile;
    this->volunteersFile = volunteersFile;
    loadDepartments();
    loadVolunteers();
    linkVolunteersToDepartments();
}

void Repository::linkVolunteersToDepartments() {
    for (auto &volunteer : volunteers) {
        if (volunteer.getDepartmentName() == "null") {
            volunteer.setDepartment(nullptr);
            continue;
        }

        bool foundDepartment = false;
        for (auto &department : departments) {
            if (volunteer.getDepartmentName() == department.getName()) {
                volunteer.setDepartment(&department);
                foundDepartment = true;
                break;
            }
        }

        if (!foundDepartment) {
            throw std::runtime_error("Volunteer " + volunteer.getName() + " has an invalid department name");
        }
    }
}

void Repository::loadDepartments() {
    std::ifstream file(departmentsFile);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open departments file");
    }

    Department department;
    while (file >> department) {
        departments.push_back(department);
    }

    file.close();
}

void Repository::loadVolunteers() {
    std::ifstream file(volunteersFile);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open volunteers file");
    }

    Volunteer volunteer;
    while (file >> volunteer) {
        volunteers.push_back(volunteer);
    }

    file.close();
}

void Repository::saveDepartments() {
    std::ofstream file(departmentsFile);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open departments file");
    }

    for (auto &department : departments) {
        file << department << "\n";
    }

    file.close();
}

void Repository::saveVolunteers() {
    std::ofstream file(volunteersFile);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open volunteers file");
    }

    for (auto &volunteer : volunteers) {
        file << volunteer << "\n";
    }

    file.close();
}

void Repository::addVolunteer(const Volunteer &volunteer) {
    volunteers.push_back(volunteer);
    saveVolunteers();
}

void Repository::assignVolunteer(const std::string &name, const std::string &email, Department *department) {
    for (auto &volunteer : volunteers) {
        if (volunteer.getName() == name && volunteer.getEmail() == email) {
            volunteer.setDepartment(department);
            volunteer.setDepartmentName(department->getName());
            saveVolunteers();
            return;
        }
    }

    throw std::runtime_error("Could not find volunteer with name " + name + " and email " + email);
}

Department *Repository::getDepartment(int index) {
    return &departments[index];
}

vector<Department> &Repository::getDepartments() {
    return this->departments;
}

vector<Volunteer> &Repository::getVolunteers() {
    return this->volunteers;
}
