//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_DEPARTMENT_H
#define VOLUNTEERING_DEPARTMENT_H

#include <string>

class Department {

private:
    std::string name;
    std::string description;

public:
    Department() : name(""), description("") {};

    Department(const std::string &name, const std::string &description) : name(name), description(description) {};

    std::string getName() const;

    std::string getDescription() const;

    void setName(const std::string &name);

    void setDescription(const std::string &description);

    bool operator==(const Department &other) const;

    bool operator!=(const Department &other) const;

    friend std::ostream &operator<<(std::ostream &os, const Department &department);

    friend std::istream &operator>>(std::istream &is, Department &department);

};


#endif //VOLUNTEERING_DEPARTMENT_H
