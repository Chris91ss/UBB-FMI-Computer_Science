#pragma once
#include <string>
#include <iostream>
using namespace std;

class Issue {
private:
    string description;
    string status;
    string reporterName;
    string solverName;
public:
    Issue() = default;
    string getDescription() const;
    string getStatus() const;
    string getReporterName() const;
    string getSolverName() const;
    void setDescription(const string& description);
    void setStatus(const string& status);
    void setReporterName(const string& reporterName);
    void setSolverName(const string& solverName);
    ~Issue() = default;
    friend ostream& operator<<(ostream& os, const Issue& issue);
    friend istream& operator>>(istream& is, Issue& issue);
    string toString();
};