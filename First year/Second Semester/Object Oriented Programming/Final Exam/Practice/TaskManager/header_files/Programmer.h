//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_PROGRAMMER_H
#define TASKMANAGER_PROGRAMMER_H

#include <string>


class Programmer {

private:
    std::string name;
    int id;

public:
    Programmer() : name(""), id(-1) {};

    Programmer(const std::string &name, int id) : name(name), id(id) {};

    std::string getName() const;

    int getId() const;

    void setName(const std::string &name);

    void setId(int id);

    bool operator==(const Programmer &other) const;

    bool operator!=(const Programmer &other) const;

    friend std::ostream &operator<<(std::ostream &os, const Programmer &programmer);

    friend std::istream &operator>>(std::istream &is, Programmer &programmer);

};


#endif //TASKMANAGER_PROGRAMMER_H
