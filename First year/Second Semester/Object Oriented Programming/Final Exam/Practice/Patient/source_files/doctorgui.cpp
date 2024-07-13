//
// Created by qdeni on 6/26/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_DoctorGui.h" resolved

#include <QMessageBox>
#include "../header_files/doctorgui.h"
#include "../form_files/ui_DoctorGui.h"
#include "../header_files/utils.h"

using namespace std;

DoctorGui::DoctorGui(QWidget *parent) :
        QWidget(parent), ui(new Ui::DoctorGui), controller(nullptr), doctor(nullptr) {
    this->ui->setupUi(this);
}

DoctorGui::~DoctorGui() {
    this->controller->unregisterObserver(this);
    delete this->ui;
}

void DoctorGui::makeConnections() {
    QObject::connect(this->ui->checkBox, &QCheckBox::stateChanged, this, &DoctorGui::update);
    QObject::connect(this->ui->addButton, &QPushButton::clicked, this, &DoctorGui::addPatient);
    QObject::connect(this->ui->patientsList, &QListWidget::itemSelectionChanged, this, &DoctorGui::selectPatient);
    QObject::connect(this->ui->updateButton, &QPushButton::clicked, this, &DoctorGui::updatePatient);
}

void DoctorGui::init(Controller *controller, Doctor *doctor) {
    this->controller = controller;
    this->doctor = doctor;
    this->controller->registerObserver(this);

    this->makeConnections();
    this->update();
    this->setWindowTitle(QString::fromStdString(this->doctor->getName()));
    this->show();
}

void DoctorGui::update() {
    vector<Patient> patients = this->controller->getPatientsBySpecialization(this->doctor->getSpecialization());
    for (const auto &patient : this->controller->getPatientsUndiagnosed()) {
        bool found = false;
        for (const auto &p : patients) {
            if (p == patient) {
                found = true;
                break;
            }
        }

        if (!found) {
            patients.push_back(patient);
        }
    }

    if (this->ui->checkBox->isChecked()) {
        patients.erase(remove_if(patients.begin(), patients.end(), [this](const Patient &patient) {
            return patient.getDoctor() != this->doctor->getName();
        }), patients.end());
    }

    sort(patients.begin(), patients.end(), [](const Patient &a, const Patient &b) {
        return a.getDate() < b.getDate();
    });

    this->ui->patientsList->clear();
    for (const auto &patient : patients) {
        this->ui->patientsList->addItem(QString::fromStdString(patient.toString()));
        if (patient.getDoctor() == this->doctor->getName()) {
            this->ui->patientsList->item(this->ui->patientsList->count() - 1)->setBackground(Qt::green);
        }
    }
}

void DoctorGui::addPatient() {
    string name = this->ui->nameLineEdit->text().toStdString();
    string diagnosis = this->ui->diagnosisLineEdit->text().toStdString();
    string specialization = this->ui->specializationLineEdit->text().toStdString();
    string doctor = this->ui->doctorLineEdit->text().toStdString();
    string date = this->ui->dateLineEdit->text().toStdString();

    try {
        this->controller->addPatient(name, diagnosis, specialization, doctor, date);
    } catch (const exception &e) {
        QMessageBox::critical(this, "Invalid patient data!", e.what());
    }
}

void DoctorGui::selectPatient() {
    if (this->ui->patientsList->selectedItems().empty()) {
        return;
    }

    string patientString = this->ui->patientsList->selectedItems()[0]->text().toStdString();
    vector<string> tokensPatient = tokenize(patientString, '|');
    string name = tokensPatient[0];
    string diagnosis = tokensPatient[1];
    string specialization = tokensPatient[2];
    string doctor = tokensPatient[3];
    vector<string> tokensDate = tokenize(tokensPatient[4], '.');
    string date = tokensDate[0] + "." + tokensDate[1] + "." + tokensDate[2];

    if (doctor != this->doctor->getName() && diagnosis != "undiagnosed") {
        QMessageBox::critical(this, "Invalid patient!", "You can only update your patients!");
        return;
    }

    this->ui->nameLineEdit->setText(QString::fromStdString(name));
    this->ui->diagnosisLineEdit->setText(QString::fromStdString(diagnosis));
    this->ui->specializationLineEdit->setText(QString::fromStdString(specialization));
    this->ui->doctorLineEdit->setText(QString::fromStdString(doctor));
    this->ui->dateLineEdit->setText(QString::fromStdString(date));
}

void DoctorGui::updatePatient() {
    string name = this->ui->nameLineEdit->text().toStdString();
    string diagnosis = this->ui->diagnosisLineEdit->text().toStdString();
    string specialization = this->ui->specializationLineEdit->text().toStdString();

    try {
        this->controller->updatePatient(name, diagnosis, specialization);
    } catch (const exception &e) {
        QMessageBox::critical(this, "Invalid patient data!", e.what());
    }
}
