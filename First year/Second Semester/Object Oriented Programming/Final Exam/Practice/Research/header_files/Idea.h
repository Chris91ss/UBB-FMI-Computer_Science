//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_IDEA_H
#define RESEARCH_IDEA_H

#include <fstream>
#include "utils.h"

class Idea {
private:
    std::string title;
    std::string description;
    std::string status;
    std::string creator;
    int duration;

public:
    Idea() : duration(-1) {}

    Idea(const std::string &title, const std::string &description, const std::string &status, const std::string &creator, int duration) {
        this->title = title;
        this->description = description;
        this->status = status;
        this->creator = creator;
        this->duration = duration;
    }

    std::string getTitle() const {
        return this->title;
    }

    std::string getDescription() const {
        return this->description;
    }

    std::string getStatus() const {
        return this->status;
    }

    std::string getCreator() const {
        return this->creator;
    }

    int getDuration() const {
        return this->duration;
    }

    void setStatus(const std::string &status) {
        this->status = status;
    }

    std::string toString() const {
        return this->title + "{ " + this->creator + " } " + std::to_string(this->duration) + " " + this->description;
    }

    friend std::ostream &operator<<(std::ostream &os, const Idea &idea) {
        os << idea.title << ";" << idea.description << ";" << idea.status << ";" << idea.creator << ";" << idea.duration;
        return os;
    }

    friend std::ifstream &operator>>(std::ifstream &is, Idea &idea) {
        std::string line;
        std::getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');
        if (tokens.size() != 5) {
            throw std::runtime_error("Invalid idea file format!");
        }

        idea.title = tokens[0];
        idea.description = tokens[1];
        idea.status = tokens[2];
        idea.creator = tokens[3];
        try {
            idea.duration = std::stoi(tokens[4]);
        } catch (std::exception &e) {
            throw std::runtime_error("Invalid idea!");
        }

        return is;
    }

};


#endif //RESEARCH_IDEA_H
