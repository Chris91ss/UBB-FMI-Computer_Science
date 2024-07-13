#pragma once
#include <vector>
#include <fstream>
#include <sstream>
#include "../domain/issue.h"
#include "../domain/user.h"

using namespace std;


class Repository {
private:
    vector<Issue*> issues;
    vector<User*> users;
public:
    Repository() = default;
    ~Repository() = default;
    void addIssue(Issue* issue);
    void addUser(User* user);
    vector<Issue*> getIssues();
    vector<User*> getUsers();
    void removeIssue(string description);
    void removeUser(User* user);
    void updateIssue(string description, string status, string reporterName, string solverName);
    void saveIssuesToFile(const string &filename);
    void saveUsersToFile(const string &filename);
    void loadIssuesFromFile(const string& filename);
    void loadUsersFromFile(const string& filename);
};