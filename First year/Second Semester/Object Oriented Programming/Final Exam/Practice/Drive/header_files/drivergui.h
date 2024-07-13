//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_DRIVERGUI_H
#define DRIVE_DRIVERGUI_H

#include <QWidget>
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class DriverGui; }
QT_END_NAMESPACE

class DriverGui : public QWidget, public Observer {
Q_OBJECT

private:
    Driver *driver;
    Controller *controller;

public:
    explicit DriverGui(QWidget *parent = nullptr);

    ~DriverGui() override;

    void init(Driver *driver, Controller *controller);

private:
    void makeConnections();

    void update();

    void sendMessage();

    void addReport();

    void validateReport();

private:
    Ui::DriverGui *ui;
};


#endif //DRIVE_DRIVERGUI_H
