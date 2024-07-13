//
// Created by qdeni on 6/28/2023.
//

#ifndef E916_DENIS916_COMPANYGUI_H
#define E916_DENIS916_COMPANYGUI_H

#include <QWidget>
#include "Session.h"


QT_BEGIN_NAMESPACE
namespace Ui { class CompanyGui; }
QT_END_NAMESPACE

class CompanyGui : public QWidget, public Observer {
Q_OBJECT

private:
    Session *session;

public:
    explicit CompanyGui(Session *session, QWidget *parent = nullptr);

    ~CompanyGui() override;

    void update() override;

private:
    void makeConnections();

    void addPackage();

private:
    Ui::CompanyGui *ui;
};


#endif //E916_DENIS916_COMPANYGUI_H
