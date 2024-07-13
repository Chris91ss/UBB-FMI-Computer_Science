//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_VOLUNTEER_H
#define VOLUNTEERING_VOLUNTEER_H

#include <vector>
#include "Department.h"

class Volunteer {

private:
    std::string name;
    std::string email;
    std::vector<std::string> interests;
    std::string departmentName;
    Department *department;

public:
    Volunteer() : name(""), email(""), interests(std::vector<std::string>()), departmentName(""), department(nullptr) {};

    Volunteer(const std::string &name, const std::string &email, const std::vector<std::string> &interests,
              const std::string &departmentName) : name(name), email(email), interests(interests),
                                                   departmentName(departmentName), department(nullptr) {};

    std::string getName() const;

    std::string getEmail() const;

    std::vector<std::string> getInterests() const;

    std::string getDepartmentName() const;

    Department *getDepartment() const;

    void setName(const std::string &name);

    void setEmail(const std::string &email);

    void setInterests(const std::vector<std::string> &interests);

    void setDepartmentName(const std::string &departmentName);

    void setDepartment(Department *department);

    bool operator==(const Volunteer &other) const;

    bool operator!=(const Volunteer &other) const;

    friend std::ostream &operator<<(std::ostream &os, const Volunteer &volunteer);

    friend std::istream &operator>>(std::istream &is, Volunteer &volunteer);

    std::string toString() const;

};


#endif //VOLUNTEERING_VOLUNTEER_H
