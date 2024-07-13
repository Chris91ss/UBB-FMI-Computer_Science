//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_REPORT_H
#define DRIVE_REPORT_H

#include "utils.h"

class Report {
private:
    std::string description;
    std::string reporter;
    std::pair<int, int> location;
    bool status;
    std::vector<std::string> validators;

public:
    Report() = default;

    Report(const std::string &description, const std::string &reporter, const std::pair<int, int> &location,
           bool status) : description(description), reporter(reporter), location(location), status(status) {};

    std::string getDescription() const {
        return this->description;
    }

    std::string getReporter() const {
        return this->reporter;
    }

    std::pair<int, int> getLocation() const {
        return this->location;
    }

    bool getStatus() const {
        return this->status;
    }

    bool validate(const std::string &validator) {
        this->validators.push_back(validator);
        if (this->validators.size() >= 2) {
            this->status = true;
            return true;
        }
        return false;
    }

    std::vector<std::string> &getValidators() {
        return this->validators;
    }

    friend std::ostream &operator<<(std::ostream &os, const Report &report) {
        os << report.description << ";" << report.reporter << ";" << report.location.first << ";"
           << report.location.second << ";";
        if (report.status) {
            os << "true";
        } else {
            os << "false";
        }
        for (auto &validator : report.validators) {
            os << ";" << validator;
        }

        return os;
    }

    friend std::istream &operator>>(std::istream &is, Report &report) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');
        if (tokens.size() < 5) {
            throw std::runtime_error("Invalid report data");
        }

        report.description = tokens[0];
        report.reporter = tokens[1];
        try {
            report.location = std::make_pair(stoi(tokens[2]), stoi(tokens[3]));
        } catch (std::exception &e) {
            throw std::runtime_error("Invalid report location");
        }
        if (tokens[4] == "true") {
            report.status = true;
        } else if (tokens[4] == "false") {
            report.status = false;
        } else {
            throw std::runtime_error("Invalid report status");
        }
        for (auto it = tokens.begin() + 5; it < tokens.end(); ++it) {
            report.validators.push_back(*it);
        }

        return is;
    }

    std::string toString() const {
        std::string result = this->description + ";" + this->reporter + ";" + std::to_string(this->location.first) + ";" +
                             std::to_string(this->location.second) + ";";

        if (this->status) {
            result += "true";
        } else {
            result += "false";
        }

        return result;
    }
};


#endif //DRIVE_REPORT_H
