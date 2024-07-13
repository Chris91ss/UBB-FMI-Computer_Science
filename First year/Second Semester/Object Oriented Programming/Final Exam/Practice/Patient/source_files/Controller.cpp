//
// Created by qdeni on 6/26/2023.
//

#include <algorithm>
#include <ctime>
#include "../header_files/Controller.h"

using namespace std;

Controller::Controller(const string &doctorsFile, const string &patientsFile) {
    this->doctorsFile = doctorsFile;
    this->patientsFile = patientsFile;
    this->loadDoctors();
    this->loadPatients();
}

void Controller::loadDoctors() {
    ifstream fin(this->doctorsFile);
    if (!fin.is_open()) {
        throw runtime_error("Could not open doctors fin!");
    }

    Doctor doctor;
    while(fin >> doctor) {
        this->doctors.push_back(doctor);
    }

    fin.close();
}

void Controller::loadPatients() {
    ifstream fin(this->patientsFile);
    if (!fin.is_open()) {
        throw runtime_error("Could not open patients fin!");
    }

    Patient patient;
    while(fin >> patient) {
        this->patients.push_back(patient);
    }

    fin.close();
}

void Controller::writePatients() {
    ofstream fout(this->patientsFile);
    if (!fout.is_open()) {
        throw runtime_error("Could not open patients fout!");
    }

    for (const auto &patient : this->patients) {
        fout << patient << endl;
    }

    fout.close();
}

void Controller::addPatient(const std::string &name, const std::string &diagnosis, const std::string &specialization,
                            const std::string &doctor, const std::string &dateString) {
    if (name.empty()) {
        throw runtime_error("Name cannot be empty!");
    }
    for (const auto &patient : this->patients) {
        if (patient.getName() == name) {
            throw runtime_error("Patient already exists!");
        }
    }

    vector<string> tokens = tokenize(dateString, '.');
    Date date;
    try {
        date.day = stoi(tokens[0]);
        date.month = stoi(tokens[1]);
        date.year = stoi(tokens[2]);
    } catch (exception &e) {
        throw runtime_error("Invalid date!");
    }

    time_t now = time(nullptr);
    tm *ltm = localtime(&now);
    if (date.year < 1900 + ltm->tm_year) {
        throw runtime_error("Date is in the past!");
    } else if (date.year == 1900 + ltm->tm_year) {
        if (date.month < 1 + ltm->tm_mon) {
            throw runtime_error("Date is in the past!");
        } else if (date.month == 1 + ltm->tm_mon) {
            if (date.day < ltm->tm_mday) {
                throw runtime_error("Date is in the past!");
            }
        }
    }

    Patient patient(name, diagnosis, specialization, doctor, date);
    this->patients.push_back(patient);
    this->writePatients();
    this->notify();
}

void Controller::updatePatient(const std::string &name, const std::string &diagnosis, const std::string &specialization) {
    if (name.empty()) {
        throw runtime_error("Patient not found!");
    }
    if (diagnosis.empty()) {
        throw runtime_error("Diagnosis cannot be empty!");
    }
    if (specialization.empty()) {
        throw runtime_error("Specialization cannot be empty!");
    }

    if (diagnosis == "undiagnosed") {
        throw runtime_error("Diagnosis cannot be undiagnosed!");
    }

    bool found = false;
    for (auto &patient : this->patients) {
        if (patient.getName() == name) {
            patient.setDiagnosis(diagnosis);
            patient.setSpecialization(specialization);
            found = true;
            break;
        }
    }

    if (!found) {
        throw runtime_error("Patient does not exist!");
    }

    this->writePatients();
    this->notify();
}

Doctor *Controller::getDoctorByIndex(int index) {
    if (index < 0 || index >= this->doctors.size()) {
        return nullptr;
    }

    return &this->doctors[index];
}

std::vector<Doctor> &Controller::getDoctors() {
    return this->doctors;
}

std::vector<Patient> &Controller::getPatients() {
    return this->patients;
}

std::vector<Patient> Controller::getPatientsBySpecialization(const std::string &specialization) {
    vector<Patient> filteredPatients;

    copy_if(this->patients.begin(), this->patients.end(), back_inserter(filteredPatients), [specialization](const Patient &patient) {
        return patient.getSpecialization() == specialization;
    });

    return filteredPatients;
}

std::vector<Patient> Controller::getPatientsUndiagnosed() {
    vector<Patient> filteredPatients;

    copy_if(this->patients.begin(), this->patients.end(), back_inserter(filteredPatients), [](const Patient &patient) {
        return patient.getDiagnosis() == "undiagnosed";
    });

    return filteredPatients;
}
