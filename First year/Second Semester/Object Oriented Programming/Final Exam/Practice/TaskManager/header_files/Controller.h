//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_CONTROLLER_H
#define TASKMANAGER_CONTROLLER_H


#include "TaskRepository.h"

class Controller {

private:
    TaskRepository repository;

public:
    Controller(TaskRepository &repository) : repository(repository) {};

    void addTask(const std::string &description, int programmerId);

    void removeTask(const std::string &description);

    Programmer &getProgrammerByIndex(int index);

    std::vector<Programmer> &getProgrammers();

    std::vector<Task> &getTasks();
};


#endif //TASKMANAGER_CONTROLLER_H
