//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_DOCTORGUI_H
#define PATIENT_DOCTORGUI_H

#include <QWidget>
#include "Observer.h"
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class DoctorGui; }
QT_END_NAMESPACE

class DoctorGui : public QWidget, public Observer {
Q_OBJECT

private:
    Controller *controller;
    Doctor *doctor;

public:
    explicit DoctorGui(QWidget *parent = nullptr);

    void init(Controller *controller, Doctor *doctor);

    ~DoctorGui() override;

private:
    void makeConnections();

    void update() override;

    void addPatient();

    void selectPatient();

    void updatePatient();

private:
    Ui::DoctorGui *ui;
};


#endif //PATIENT_DOCTORGUI_H
