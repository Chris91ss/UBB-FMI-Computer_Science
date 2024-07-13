#include "service.h"
#include <algorithm>

void Service::addIssueToRepo(Issue *issue) {
    for(Issue *i: repository->getIssues())
        if(i->getDescription() == issue->getDescription())
            throw runtime_error("Issue already exists!");
    repository->addIssue(issue);
    notify();
}

void Service::addUserToRepo(User *user) {
    repository->addUser(user);
    notify();
}

vector<Issue *> Service::getIssuesFromRepo() {
    return repository->getIssues();
}

vector<Issue *> Service::sortByStatusAndDescription() {
    vector<Issue *> issues = repository->getIssues();
    sort(issues.begin(), issues.end(), [](Issue *a, Issue *b) {
        if (a->getDescription() == b->getDescription()) {
            return a->getStatus() < b->getStatus();
        }
        return a->getDescription() < b->getDescription();
    });
    return issues;
}

vector<User *> Service::getUsersFromRepo() {
    return repository->getUsers();
}

void Service::removeIssueFromRepo(string description) {
    repository->removeIssue(description);
    notify();
}

void Service::removeUserFromRepo(User *user) {
    repository->removeUser(user);
    notify();
}

void Service::updateIssueInRepo(string description, string status, string reporterName, string solverName) {
    repository->updateIssue(description, status, reporterName, solverName);
    notify();
}

void Service::saveIssuesToFile(const string &filename) {
    repository->saveIssuesToFile(filename);
}

void Service::saveUsersToFile(const string &filename) {
    repository->saveUsersToFile(filename);
}