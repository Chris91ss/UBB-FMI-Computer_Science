//
// Created by Chris on 6/19/2024.
//

#ifndef GUI_H
#define GUI_H

#include <QWidget>

#include "observer.h"
#include "service/service.h"


QT_BEGIN_NAMESPACE
namespace Ui { class GUI; }
QT_END_NAMESPACE

class GUI : public QWidget, public Observer{
Q_OBJECT

public:
    explicit GUI(QWidget *parent = nullptr, Service *service = nullptr, User *user = nullptr);
    ~GUI() override;

private:
    Ui::GUI *ui;

    Service *service;
    User *user;

    void updateList();
    void addIssue();
    void removeIssue();
    void resolveIssue();
    void onSelectionChanged();
    void update () override;
};


#endif //GUI_H
