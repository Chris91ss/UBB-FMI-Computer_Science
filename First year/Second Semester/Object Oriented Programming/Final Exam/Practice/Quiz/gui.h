//
// Created by Adrian Trill on 21.06.2024.
//

#ifndef QUIZ_GUI_H
#define QUIZ_GUI_H

#include <QWidget>
#include "service/service.h"


QT_BEGIN_NAMESPACE
namespace Ui { class gui; }
QT_END_NAMESPACE

class gui : public QWidget, public Observer{
Q_OBJECT

public:
    explicit gui(QWidget *parent = nullptr, Service *service = nullptr, Participant *participant = nullptr);

    ~gui() override;

private:
    Ui::gui *ui;

    Service *service;
    Participant *participant;
public:
    void updateListPresenter();
    void updateListParticipant();
    void addQuestion();
    void update() override;
};


#endif //QUIZ_GUI_H
