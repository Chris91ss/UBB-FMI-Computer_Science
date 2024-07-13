//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_TASK_H
#define TASKMANAGER_TASK_H

#include <string>

class Task {

private:
    std::string description;
    std::string status;
    int programmerId;

public:
    Task() : description(""), status(""), programmerId(-1) {};

    Task(const std::string &description, const std::string &status, int programmerId) : description(description),
                                                                                        status(status),
                                                                                        programmerId(programmerId) {};

    std::string getDescription() const;

    std::string getStatus() const;

    int getProgrammerId() const;

    void setDescription(const std::string &description);

    void setStatus(const std::string &status);

    void setProgrammerId(int programmerId);

    bool operator==(const Task &other) const;

    bool operator!=(const Task &other) const;

    friend std::ostream &operator<<(std::ostream &os, const Task &task);

    friend std::istream &operator>>(std::istream &is, Task &task);

};


#endif //TASKMANAGER_TASK_H
