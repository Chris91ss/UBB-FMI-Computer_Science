//
// Created by Adrian Trill on 20.06.2024.
//

#ifndef OOP_PRACTICE_GUI_H
#define OOP_PRACTICE_GUI_H

#include <QWidget>
#include "service/service.h"


QT_BEGIN_NAMESPACE
namespace Ui { class gui; }
QT_END_NAMESPACE

class gui : public QWidget, public Observer{
Q_OBJECT

public:
    explicit gui(QWidget *parent = nullptr, Service *service = nullptr, Person *person = nullptr);

    ~gui() override;

private:
    Ui::gui *ui;
    Service *service;
    Person *person;

    void populateList();
    void showEventsNearPerson();
    void addEvent();
    void eventSelected();
    void updateEvent();
    void updateAttendeesList(const string &eventName);
    void update() override;

private slots:
    void onGoingButtonClicked();




};


#endif //OOP_PRACTICE_GUI_H
