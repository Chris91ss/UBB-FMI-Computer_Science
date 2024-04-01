#include "service/service.h"

Service::Service(Repository<Task> &repository) {
    this->repository = repository;
}

Service::Service(const Service &other) {
    this->repository = other.repository;
}

Service::~Service() = default;

Service &Service::operator=(const Service &other) {
    this->repository = other.repository;
    return *this;
}

void Service::AddTask(const string &description, int duration, int priority) {
    Task task = Task(description, duration, priority);
    if(this->repository.search(task)) {
        throw runtime_error("Task already exists\n");
    }
    this->repository.add(task);
}

DynamicVector<Task> Service::GetAllTasks() const {
    return this->repository.getAll();
}

void Service::Generate5Tasks() {
    this->AddTask("Task1", 1, 1);
    this->AddTask("Task2", 2, 2);
    this->AddTask("Task3", 3, 3);
    this->AddTask("Task4", 4, 4);
    this->AddTask("Task5", 5, 5);
}

DynamicVector<Task> Service::GetTasksFilteredAndSorted(int priority) const {
    DynamicVector<Task> tasks = this->repository.getAll();
    DynamicVector<Task> filteredTasks;
    for(int i = 0; i < tasks.GetSizeOfDynamicVector(); i++) {
        if(tasks[i].getPriority() < priority) {
            filteredTasks.AddToDynamicVector(tasks[i]);
        }
    }
    for(int i = 0; i < filteredTasks.GetSizeOfDynamicVector() - 1; i++) {
        for(int j = i + 1; j < filteredTasks.GetSizeOfDynamicVector(); j++) {
            if(filteredTasks[i].getDuration() < filteredTasks[j].getDuration()) {
                Task aux = filteredTasks[i];
                filteredTasks[i] = filteredTasks[j];
                filteredTasks[j] = aux;
            }
        }
    }
    return filteredTasks;
}



