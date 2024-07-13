//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_STATISTICGUI_H
#define PATIENT_STATISTICGUI_H

#include <QWidget>
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class StatisticGui; }
QT_END_NAMESPACE

class StatisticGui : public QWidget, public Observer {
Q_OBJECT

private:
    Controller &controller;

public:
    explicit StatisticGui(Controller &controller, QWidget *parent = nullptr);

    ~StatisticGui() override;

private:
    void update() override;

    void paintEvent(QPaintEvent *event) override;

private:
    Ui::StatisticGui *ui;
};


#endif //PATIENT_STATISTICGUI_H
