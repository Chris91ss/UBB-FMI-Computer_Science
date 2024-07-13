#include "repository.h"

void Repository::addIssue(Issue *issue) {
    issues.push_back(issue);
    saveIssuesToFile("../data/issue.txt");
}

void Repository::addUser(User *user) {
    users.push_back(user);
    saveUsersToFile("../data/user.txt");
}

vector<Issue *> Repository::getIssues() {
    return issues;
}

vector<User *> Repository::getUsers() {
    return users;
}

void Repository::removeIssue(string description) {
    for (int i = 0; i < issues.size(); i++) {
        if (issues[i]->getDescription() == description) {
            issues.erase(issues.begin() + i);
            saveIssuesToFile("../data/issue.txt");
            return;
        }
    }
}

void Repository::removeUser(User *user) {
    for(int i = 0; i < users.size(); i++) {
        if (users[i] == user) {
            users.erase(users.begin() + i);
            saveUsersToFile("../data/user.txt");
            return;
        }
    }
}

void Repository::updateIssue(string description, string status, string reporterName, string solverName) {
    for(auto& issue : issues) {
        if (issue->getDescription() == description) {
            issue->setStatus(status);
            issue->setReporterName(reporterName);
            issue->setSolverName(solverName);
            saveIssuesToFile("../data/issue.txt");
            return;
        }
    }
}

void Repository::saveIssuesToFile(const string &filename) {
    ofstream outFile(filename);
    if (outFile.is_open()) {
        for (const auto& issue : issues) {
            outFile << *issue << endl;
        }
        outFile.close();
    } else {
        cerr << "Could not open file for writing: " << filename << endl;
    }
}

void Repository::saveUsersToFile(const string &filename) {
    ofstream outFile(filename);
    if (outFile.is_open()) {
        for (const auto& user : users) {
            outFile << *user << endl;
        }
        outFile.close();
    } else {
        cerr << "Could not open file for writing: " << filename << endl;
    }
}

void Repository::loadIssuesFromFile(const string& filename) {
    ifstream inFile(filename);
    if (inFile.is_open()) {
        string line;
        while (getline(inFile, line)) {
            istringstream iss(line);
            Issue* issue = new Issue();
            iss >> *issue;
            addIssue(issue);
        }
        inFile.close();
    } else {
        cerr << "Could not open file for reading: " << filename << endl;
    }
}

void Repository::loadUsersFromFile(const string& filename) {
    ifstream inFile(filename);
    if (inFile.is_open()) {
        string line;
        while (getline(inFile, line)) {
            istringstream iss(line);
            User* user = new User();
            iss >> *user;
            addUser(user);
        }
        inFile.close();
    } else {
        cerr << "Could not open file for reading: " << filename << endl;
    }
}
