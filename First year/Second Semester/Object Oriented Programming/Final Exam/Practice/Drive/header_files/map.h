//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_MAP_H
#define DRIVE_MAP_H

#include <QWidget>
#include "Observer.h"
#include "Controller.h"


QT_BEGIN_NAMESPACE
namespace Ui { class Map; }
QT_END_NAMESPACE

class Map : public QWidget, public Observer {
Q_OBJECT

private:
    Controller &controller;

public:
    explicit Map(Controller &controller, QWidget *parent = nullptr);

    ~Map() override;

private:
    Ui::Map *ui;

    void update() override;

    void paintEvent(QPaintEvent *event) override;
};


#endif //DRIVE_MAP_H
