//
// Created by qdeni on 6/28/2023.
//

#ifndef E916_DENIS916_COURIERGUI_H
#define E916_DENIS916_COURIERGUI_H

#include <QWidget>
#include "Session.h"


QT_BEGIN_NAMESPACE
namespace Ui { class CourierGui; }
QT_END_NAMESPACE

class CourierGui : public QWidget, public Observer {
Q_OBJECT

private:
    Session *session;
    Courier *courier;

public:
    explicit CourierGui(Courier *courier, Session *session, QWidget *parent = nullptr);

    ~CourierGui() override;

    void update() override;

private:
    void makeConnections();

    void selectStreet();

    void deliverPackage();

private:
    Ui::CourierGui *ui;
};


#endif //E916_DENIS916_COURIERGUI_H
