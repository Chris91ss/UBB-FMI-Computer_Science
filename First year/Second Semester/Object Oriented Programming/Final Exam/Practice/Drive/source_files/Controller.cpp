//
// Created by qdeni on 6/27/2023.
//

#include "../header_files/Controller.h"
#include <cmath>

using namespace std;

int distance(const pair<int, int> &a, const pair<int, int> &b) {
    return int(sqrt(pow(a.first - b.first, 2) + pow(a.second - b.second, 2)));
}

Controller::Controller(const std::string &driversFile, const std::string &reportsFile) {
    this->driversFile = driversFile;
    this->reportsFile = reportsFile;
    loadDrivers();
    loadReports();
}

void Controller::loadDrivers() {
    ifstream fin(this->driversFile);
    if (!fin.is_open()) {
        throw std::runtime_error("Could not open drivers file");
    }

    Driver driver;
    while (fin >> driver)  {
        this->drivers.push_back(driver);
    }

    fin.close();
}

void Controller::loadReports() {
    ifstream fin(this->reportsFile);
    if (!fin.is_open()) {
        throw std::runtime_error("Could not open reports file");
    }

    Report report;
    while (fin >> report) {
        this->reports.push_back(report);
    }

    fin.close();
}

void Controller::saveDrivers() {
    ofstream fout(this->driversFile);
    if (!fout.is_open()) {
        throw std::runtime_error("Could not open drivers file");
    }

    for (const auto &driver : this->drivers) {
        fout << driver << endl;
    }

    fout.close();
}

void Controller::saveReports() {
    ofstream fout(this->reportsFile);
    if (!fout.is_open()) {
        throw std::runtime_error("Could not open reports file");
    }

    for (const auto &report : this->reports) {
        fout << report << endl;
    }

    fout.close();
}

void Controller::addMessage(const std::string &text, const std::string &sender, const std::string &time) {
    Message message(text, sender, time);
    this->messages.push_back(message);
    this->notify();
}

void Controller::addReport(const std::string &description, const std::string &reporter, std::pair<int, int> location,
                           bool status, std::pair<int, int> driverLocation) {
    if (description.empty()) {
        throw std::runtime_error("Description cannot be empty");
    }
    if (distance(location, driverLocation) > 20) {
        throw std::runtime_error("Driver is too far away");
    }

    Report report(description, reporter, location, status);
    this->reports.push_back(report);
    this->saveReports();
    this->notify();
}

void Controller::validateReport(const std::string &description, const std::string &reporter,
                                std::pair<int, int> location, const std::string &validator) {
    if (validator == reporter) {
        throw std::runtime_error("Driver cannot validate his own report");
    }

    for (auto &report : this->reports) {
        if (report.getDescription() == description && report.getReporter() == reporter &&
            report.getLocation() == location) {

            if (report.getStatus()) {
                throw std::runtime_error("Report is already validated");
            }
            for (const auto &v : report.getValidators()) {
                if (v == validator) {
                    throw std::runtime_error("Driver already validated this report");
                }
            }

            if (report.validate(validator)) {
                for (auto &driver : this->drivers) {
                    if (driver.getName() == reporter) {
                        driver.setScore(driver.getScore() + 1);
                        break;
                    }
                }
            }
            this->saveReports();
            this->saveDrivers();
            this->notify();
            return;
        }
    }
}

Driver &Controller::getDriverByIndex(int index) {
    return this->drivers[index];
}

vector<Driver> &Controller::getDrivers() {
    return this->drivers;
}

vector<Report> &Controller::getReports() {
    return this->reports;
}

std::vector<Report> Controller::getNearbyReports(const pair<int, int> &location, int radius) {
    vector<Report> nearbyReports;

    for (const auto &report : this->reports) {
        if (distance(location, report.getLocation()) <= radius) {
            nearbyReports.push_back(report);
        }
    }

    return nearbyReports;
}

std::vector<Message> &Controller::getMessages() {
    return this->messages;
}
