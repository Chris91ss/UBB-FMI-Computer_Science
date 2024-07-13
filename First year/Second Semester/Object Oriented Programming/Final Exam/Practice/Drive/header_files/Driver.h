//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_DRIVER_H
#define DRIVE_DRIVER_H

#include <fstream>
#include "utils.h"

class Driver {
private:
    std::string name;
    std::pair<int, int> location;
    int score;

public:
    Driver() = default;

    std::string getName() const {
        return this->name;
    }

    std::pair<int, int> getLocation() const {
        return this->location;
    }

    int getScore() const {
        return this->score;
    }

    void setScore(int score) {
        this->score = score;
    }

    friend std::ostream &operator<<(std::ostream &os, const Driver &driver) {
        os << driver.name << ";" << driver.location.first << ";" << driver.location.second << ";" << driver.score;

        return os;
    }

    friend std::istream &operator>>(std::istream &is, Driver &driver) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');
        if (tokens.size() != 4) {
            throw std::runtime_error("Invalid driver data");
        }

        driver.name = tokens[0];
        try {
            driver.location = std::make_pair(stoi(tokens[1]), stoi(tokens[2]));
            driver.score = stoi(tokens[3]);
        } catch (std::exception &e) {
            throw std::runtime_error("Invalid driver location");
        }

        return is;
    }
};


#endif //DRIVE_DRIVER_H
