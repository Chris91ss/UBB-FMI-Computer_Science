//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_RESEARCHER_H
#define RESEARCH_RESEARCHER_H

#include <fstream>
#include <string>
#include "utils.h"

class Researcher {
private:
    std::string name;
    std::string position;

public:
    Researcher() = default;

    Researcher(const std::string &name, const std::string &position) : name(name), position(position) {};

    std::string getName() const {
        return this->name;
    }

    std::string getPosition() const {
        return this->position;
    }

    friend std::ifstream &operator>>(std::ifstream &is, Researcher &researcher) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');
        if (tokens.size() != 2) {
            throw std::runtime_error("Invalid researcher file format!");
        }

        researcher.name = tokens[0];
        researcher.position = tokens[1];

        return is;
    }
};


#endif //RESEARCH_RESEARCHER_H
