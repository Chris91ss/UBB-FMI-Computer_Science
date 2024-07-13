#include "issue.h"

string Issue::getDescription() const {
    return description;
}

string Issue::getStatus() const {
    return status;
}

string Issue::getReporterName() const {
    return reporterName;
}

string Issue::getSolverName() const {
    return solverName;
}

void Issue::setDescription(const string &description) {
    this->description = description;
}

void Issue::setStatus(const string &status) {
    this->status = status;
}

void Issue::setReporterName(const string &reporterName) {
    this->reporterName = reporterName;
}

void Issue::setSolverName(const string &solverName) {
    this->solverName = solverName;
}

string Issue::toString() {
    return description + ";" + status + ";" + reporterName + ";" + solverName;
}

ostream & operator<<(ostream &os, const Issue &issue) {
    os << issue.description << ";" << issue.status << ";" << issue.reporterName << ";" << issue.solverName;
    return os;
}

istream & operator>>(istream &is, Issue &issue) {
    getline(is, issue.description, ';');
    getline(is, issue.status, ';');
    getline(is, issue.reporterName, ';');
    getline(is, issue.solverName);
    return is;
}


