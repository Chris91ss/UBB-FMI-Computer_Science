#pragma once
#include "../subject.h"
#include "../repository/repository.h"

class Service: public Subject{
private:
    Repository *repository;
public:
    Service(Repository *repository): repository(repository) {
        repository->loadIssuesFromFile("../data/issue.txt");
        repository->loadUsersFromFile("../data/user.txt");
    }
    ~Service() = default;
    void addIssueToRepo(Issue *issue);
    void addUserToRepo(User *user);
    vector<Issue *> getIssuesFromRepo();
    vector<Issue *> sortByStatusAndDescription();
    vector<User *> getUsersFromRepo();
    void removeIssueFromRepo(string description);
    void removeUserFromRepo(User *user);
    void updateIssueInRepo(string description, string status, string reporterName, string solverName);
    void saveIssuesToFile(const string &filename);
    void saveUsersToFile(const string &filename);
};
