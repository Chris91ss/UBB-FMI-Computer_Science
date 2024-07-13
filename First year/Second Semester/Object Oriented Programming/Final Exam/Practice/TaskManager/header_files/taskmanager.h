//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_TASKMANAGER_H
#define TASKMANAGER_TASKMANAGER_H

#include <QWidget>
#include <QAbstractItemModel>
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class TaskManager; }
QT_END_NAMESPACE

class TaskManager : public QWidget {
Q_OBJECT

private:
    QAbstractItemModel *model;
    Controller *controller;
    Programmer *programmer;

public:
    TaskManager(QWidget *parent = nullptr);

    ~TaskManager() override;

    void makeConnections();

    void init(QAbstractItemModel *model, Controller *controller, Programmer *programmer);

    void addTask();

private:
    Ui::TaskManager *ui;
};


#endif //TASKMANAGER_TASKMANAGER_H
