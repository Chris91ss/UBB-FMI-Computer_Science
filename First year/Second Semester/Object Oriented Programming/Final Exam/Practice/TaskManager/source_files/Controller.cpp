//
// Created by qdeni on 6/25/2023.
//

#include <stdexcept>
#include "../header_files/Controller.h"

void Controller::addTask(const std::string &description, int programmerId) {
    if (description.empty()) {
        throw std::runtime_error("Description cannot be empty!");
    }

    Task task(description, "open", programmerId);
    this->repository.addTask(task);
}

void Controller::removeTask(const std::string &description) {
    this->repository.removeTask(description);
}

Programmer &Controller::getProgrammerByIndex(int index) {
    return this->repository.getProgrammers()[index];
}

std::vector<Programmer> &Controller::getProgrammers() {
    return this->repository.getProgrammers();
}

std::vector<Task> &Controller::getTasks() {
    return this->repository.getTasks();
}
