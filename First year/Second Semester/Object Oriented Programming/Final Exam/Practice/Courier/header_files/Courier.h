#ifndef E916_DENIS916_COURIER_H
#define E916_DENIS916_COURIER_H

#include "utils.h"

class Courier {
private:
    std::string name;
    std::vector<std::string> streets;
    int x;
    int y;
    int radius;

public:
    Courier() = default;

    Courier(const std::string &name, std::vector<std::string> streets, int x, int y, int radius) {
        this->name = name;
        this->streets = streets;
        this->x = x;
        this->y = y;
        this->radius = radius;
    }

    std::string getName() const {
        return this->name;
    }

    std::vector<std::string> &getStreets() {
        return this->streets;
    }

    int getX() {
        return this->x;
    }

    int getY() {
        return this->y;
    }

    int getRadius() {
        return this->radius;
    }

    bool isInside(int x, int y) {
        return (this->x - x) * (this->x - x) + (this->y - y) * (this->y - y) <= this->radius * this->radius;
    }

    friend std::ifstream &operator>>(std::ifstream &is, Courier &courier) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');
        if (tokens.size() < 4) {
            throw std::runtime_error("Invalid courier data");
        }

        courier.name = tokens[0];
        try {
            courier.x = stoi(tokens[1]);
            courier.y = stoi(tokens[2]);
            courier.radius = stoi(tokens[3]);
        } catch (const std::exception &e) {
            throw std::runtime_error("Invalid courier data");
        }
        for (int i = 4; i < tokens.size(); i++) {
            courier.streets.push_back(tokens[i]);
        }

        return is;
    }

    void reset() {
        this->streets.clear();
    }
};


#endif //E916_DENIS916_COURIER_H
