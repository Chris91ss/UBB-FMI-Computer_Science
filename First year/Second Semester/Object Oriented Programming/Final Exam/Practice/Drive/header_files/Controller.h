//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_CONTROLLER_H
#define DRIVE_CONTROLLER_H

#include "Subject.h"
#include "Driver.h"
#include "Report.h"
#include "Message.h"

class Controller : public Subject {
private:
    std::vector<Driver> drivers;
    std::vector<Report> reports;
    std::vector<Message> messages;
    std::string driversFile;
    std::string reportsFile;

public:
    Controller(const std::string &driversFile, const std::string &reportsFile);

    void addMessage(const std::string &text, const std::string &sender, const std::string &time);

    void addReport(const std::string &description, const std::string &reporter, std::pair<int, int> location,
                   bool status, std::pair<int, int> driverLocation);

    void validateReport(const std::string &description, const std::string &reporter, std::pair<int, int> location,
                        const std::string &validator);

    Driver &getDriverByIndex(int index);

    std::vector<Driver> &getDrivers();

    std::vector<Report> &getReports();

    std::vector<Report> getNearbyReports(const std::pair<int, int> &location, int radius);

    std::vector<Message> &getMessages();

private:
    void loadDrivers();

    void loadReports();

    void saveDrivers();

    void saveReports();
};


#endif //DRIVE_CONTROLLER_H
