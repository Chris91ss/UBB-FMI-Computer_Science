//
// Created by qdeni on 6/25/2023.
//

#include <fstream>
#include <algorithm>
#include "../header_files/TaskRepository.h"

using namespace std;

TaskRepository::TaskRepository(const string &programmersFile, const string &tasksFile) {
    this->programmersFile = programmersFile;
    this->tasksFile = tasksFile;

    this->loadProgrammers();
    this->loadTasks();
}

void TaskRepository::addTask(const Task &task) {
    if (find(this->tasks.begin(), this->tasks.end(), task) != this->tasks.end()) {
        throw runtime_error("Task already exists");
    }

    this->tasks.push_back(task);
    this->saveTasks();
}

void TaskRepository::removeTask(const std::string &description) {
    for (auto it = this->tasks.begin(); it != this->tasks.end(); ++it) {
        if (it->getDescription() == description) {
            this->tasks.erase(it);
            this->saveTasks();
            return;
        }
    }

    throw runtime_error("Task not found");
}

Programmer &TaskRepository::getProgrammerById(int id) {
    for (auto &programmer : this->programmers) {
        if (programmer.getId() == id) {
            return programmer;
        }
    }

    throw runtime_error("Programmer not found");
}

vector<Programmer> &TaskRepository::getProgrammers() {
    return this->programmers;
}

vector<Task> &TaskRepository::getTasks() {
    return this->tasks;
}

void TaskRepository::loadProgrammers() {
    ifstream file(this->programmersFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open programmers file");
    }

    Programmer programmer;
    while (file >> programmer) {
        this->programmers.push_back(programmer);
    }

    file.close();
}

void TaskRepository::loadTasks() {
    ifstream file(this->tasksFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open tasks file");
    }

    Task task;
    while (file >> task) {
        this->tasks.push_back(task);
    }

    file.close();
}

void TaskRepository::saveProgrammers() {
    ofstream file(this->programmersFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open programmers file");
    }

    for (const auto &programmer : this->programmers) {
        file << programmer << endl;
    }

    file.close();
}

void TaskRepository::saveTasks() {
    ofstream file(this->tasksFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open tasks file");
    }

    for (auto &task : this->tasks) {
        file << task << endl;
    }

    file.close();
}
