//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include "../header_files/Task.h"
#include "../header_files/utils.h"

std::string Task::getDescription() const {
    return this->description;
}

std::string Task::getStatus() const {
    return this->status;
}

int Task::getProgrammerId() const {
    return this->programmerId;
}

void Task::setDescription(const std::string &description) {
    this->description = description;
}

void Task::setStatus(const std::string &status) {
    this->status = status;
}

void Task::setProgrammerId(int programmerId) {
    this->programmerId = programmerId;
}

bool Task::operator==(const Task &other) const {
    return this->description == other.description;
}

bool Task::operator!=(const Task &other) const {
    return !(*this == other);
}

std::ostream &operator<<(std::ostream &os, const Task &task) {
    os << task.description << "," << task.status << "," << task.programmerId;
    return os;
}

std::istream &operator>>(std::istream &is, Task &task) {
    std::string line;
    getline(is, line);

    std::vector<std::string> tokens = tokenize(line, ',');
    if (tokens.size() != 3) {
        return is;
    }

    task.setDescription(tokens[0]);
    task.setStatus(tokens[1]);
    try {
        task.setProgrammerId(stoi(tokens[2]));
    } catch (std::exception &e) {
        return is;
    }

    return is;
}
