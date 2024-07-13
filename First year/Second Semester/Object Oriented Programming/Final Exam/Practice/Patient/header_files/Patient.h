//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_PATIENT_H
#define PATIENT_PATIENT_H

#include <fstream>
#include "utils.h"

typedef struct DateAux{
    int day;
    int month;
    int year;

    DateAux() = default;

    DateAux(int day, int month, int year) {
        this->day = day;
        this->month = month;
        this->year = year;
    }

    bool operator<(const DateAux &other) const {
        if (this->year < other.year) {
            return true;
        } else if (this->year == other.year) {
            if (this->month < other.month) {
                return true;
            } else if (this->month == other.month) {
                if (this->day < other.day) {
                    return true;
                }
            }
        }
        return false;
    }

    bool operator>(const DateAux &other) const {
        return other < *this;
    }

} Date;


class Patient {
private:
    std::string name;
    std::string diagnosis;
    std::string specialization;
    std::string doctor;
    Date date;

public:
    Patient() = default;

    Patient(const std::string &name, const std::string &diagnosis, const std::string &specialization, const std::string &doctor, const Date &date) {
        this->name = name;
        this->diagnosis = diagnosis;
        this->specialization = specialization;
        this->doctor = doctor;
        this->date = date;
    }

    std::string getName() const {
        return this->name;
    }

    std::string getDiagnosis() const {
        return this->diagnosis;
    }

    std::string getSpecialization() const {
        return this->specialization;
    }

    std::string getDoctor() const {
        return this->doctor;
    }

    Date getDate() const {
        return this->date;
    }

    void setDiagnosis(const std::string &diagnosis) {
        this->diagnosis = diagnosis;
    }

    void setSpecialization(const std::string &specialization) {
        this->specialization = specialization;
    }

    friend std::ifstream &operator>>(std::ifstream &is, Patient &patient) {
        std::string line;
        getline(is, line);
        if (line.empty()) {
            return is;
        }

        std::vector<std::string> tokens = tokenize(line, ';');

        patient.name = tokens[0];
        patient.diagnosis = tokens[1];
        patient.specialization = tokens[2];
        patient.doctor = tokens[3];
        patient.date.day = stoi(tokens[4]);
        patient.date.month = stoi(tokens[5]);
        patient.date.year = stoi(tokens[6]);

        return is;
    }

    friend std::ostream &operator<<(std::ostream &os, const Patient &patient) {
        os << patient.name << ";" << patient.diagnosis << ";" << patient.specialization << ";" << patient.doctor << ";"
           << patient.date.day << ";" << patient.date.month << ";" << patient.date.year;

        return os;
    }

    std::string toString() const {
        return this->name + " | " + this->diagnosis + " | " + this->specialization + " | " + this->doctor
               + " | " + std::to_string(this->date.day) + "." + std::to_string(this->date.month) + "." + std::to_string(this->date.year);
    }

    bool operator==(const Patient &other) const {
        return this->name == other.name;
    }

};


#endif //PATIENT_PATIENT_H
