//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_DEPARTMENTGUI_H
#define VOLUNTEERING_DEPARTMENTGUI_H

#include <QWidget>
#include "Department.h"
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class DepartmentGui; }
QT_END_NAMESPACE

class DepartmentGui : public QWidget, public Observer {
Q_OBJECT

private:
    Controller *controller;
    Department *department;

public:
    explicit DepartmentGui(QWidget *parent = nullptr);

    ~DepartmentGui() override;

    void makeConnections();

    void init(Controller *controller, Department *department);

    void update() override;

    void updateVolunteersList();

    void updateUnassignedList();

    void addVolunteer();

    void showSuitable();

    void assignVolunteer();

private:
    Ui::DepartmentGui *ui;
};


#endif //VOLUNTEERING_DEPARTMENTGUI_H
