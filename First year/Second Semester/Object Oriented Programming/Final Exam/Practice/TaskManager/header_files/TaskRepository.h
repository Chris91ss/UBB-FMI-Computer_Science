//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_TASKREPOSITORY_H
#define TASKMANAGER_TASKREPOSITORY_H

#include <vector>
#include "Task.h"
#include "Programmer.h"


class TaskRepository {

private:
    std::vector<Programmer> programmers;
    std::vector<Task> tasks;
    std::string programmersFile;
    std::string tasksFile;

public:
    TaskRepository(const std::string &programmersFile, const std::string &tasksFile);

    void addTask(const Task &task);

    void removeTask(const std::string &description);

    Programmer &getProgrammerById(int id);

    std::vector<Programmer> &getProgrammers();

    std::vector<Task> &getTasks();

private:
    void loadProgrammers();

    void loadTasks();

    void saveProgrammers();

    void saveTasks();

};


#endif //TASKMANAGER_TASKREPOSITORY_H
