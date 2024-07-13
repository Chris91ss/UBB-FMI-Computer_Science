//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_CONTROLLER_H
#define PATIENT_CONTROLLER_H

#include "Subject.h"
#include "Patient.h"
#include "Doctor.h"

class Controller : public Subject {
private:
    std::vector<Doctor> doctors;
    std::vector<Patient> patients;
    std::string doctorsFile;
    std::string patientsFile;

public:
    Controller(const std::string &doctorsFile, const std::string &patientsFile);

    void addPatient(const std::string &name, const std::string &diagnosis, const std::string &specialization, const std::string &doctor, const std::string &dateString);

    void updatePatient(const std::string &name, const std::string &diagnosis, const std::string &specialization);

    Doctor *getDoctorByIndex(int index);

    std::vector<Doctor> &getDoctors();

    std::vector<Patient> &getPatients();

    std::vector<Patient> getPatientsBySpecialization(const std::string &specialization);

    std::vector<Patient> getPatientsUndiagnosed();

private:
    void loadDoctors();

    void loadPatients();

    void writePatients();
};


#endif //PATIENT_CONTROLLER_H
