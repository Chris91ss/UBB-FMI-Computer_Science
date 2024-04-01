#include "task.h"
#include "repository/repository.h"

class Service {
private:
    Repository<Task> repository;
public:
    Service(Repository<Task> &repository);
    Service(const Service &other);
    ~Service();
    Service &operator=(const Service &other);

    void AddTask(const string &description, int duration, int priority);
    DynamicVector<Task> GetAllTasks() const;
    void Generate5Tasks();
    DynamicVector<Task> GetTasksFilteredAndSorted(int priority) const;
};