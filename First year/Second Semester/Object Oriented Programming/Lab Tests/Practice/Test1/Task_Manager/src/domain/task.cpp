#include "task.h"

Task::Task() {
    this->description = "";
    this->duration = 0;
    this->priority = 0;
}

Task::Task(const string& description, int duration, int priority)
{
    this->description = description;
    this->duration = duration;
    this->priority = priority;
}

Task::Task(const Task &task) {
    this->description = task.description;
    this->duration = task.duration;
    this->priority = task.priority;
}

Task::~Task() = default;

Task &Task::operator=(const Task &task) = default;

bool Task::operator==(const Task &task) {
    return this->description == task.description;
}

string Task::getDescription() {
    return this->description;
}

int Task::getDuration() {
    return this->duration;
}

int Task::getPriority() {
    return this->priority;
}

void Task::setDescription(string newDescription) {
    this->description = newDescription;
}

void Task::setDuration(int newDuration) {
    this->duration = newDuration;
}

void Task::setPriority(int newPriority) {
    this->priority = newPriority;
}
