#pragma once
#include <string>
using namespace std;

class Task{
private:
    string description;
    int duration;
    int priority;

public:
    Task();
    Task(const string& description, int duration, int priority);
    Task(const Task &task);
    ~Task();
    Task &operator=(const Task &task);
    bool operator==(const Task &task);

    string getDescription();
    int getDuration();
    int getPriority();

    void setDescription(string newDescription);
    void setDuration(int newDuration);
    void setPriority(int newPriority);
};