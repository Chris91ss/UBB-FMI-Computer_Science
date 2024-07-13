//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_DEPARTMENTSOVERVIEW_H
#define VOLUNTEERING_DEPARTMENTSOVERVIEW_H

#include <QWidget>
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class DepartmentsOverview; }
QT_END_NAMESPACE

class DepartmentsOverview : public QWidget, public Observer {
Q_OBJECT

private:
    Controller &controller;

public:
    explicit DepartmentsOverview(Controller &controller, QWidget *parent = nullptr);

    void update() override;

    void updateList();

    ~DepartmentsOverview() override;

private:
    Ui::DepartmentsOverview *ui;
};


#endif //VOLUNTEERING_DEPARTMENTSOVERVIEW_H
