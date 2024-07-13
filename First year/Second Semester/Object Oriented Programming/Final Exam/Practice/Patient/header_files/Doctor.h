//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_DOCTOR_H
#define PATIENT_DOCTOR_H

#include <fstream>
#include "utils.h"

class Doctor {
private:
    std::string name;
    std::string specialization;

public:
    Doctor() = default;

    Doctor(const std::string &name, const std::string &specialization) {
        this->name = name;
        this->specialization = specialization;
    }

    std::string getName() const {
        return this->name;
    }

    std::string getSpecialization() const {
        return this->specialization;
    }

    friend std::ifstream &operator>>(std::ifstream &is, Doctor &doctor) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');

        doctor.name = tokens[0];
        doctor.specialization = tokens[1];

        return is;
    }

};


#endif //PATIENT_DOCTOR_H
