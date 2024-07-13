//
// Created by qdeni on 6/28/2023.
//

#ifndef E916_DENIS916_MAP_H
#define E916_DENIS916_MAP_H

#include <QWidget>
#include "Session.h"


QT_BEGIN_NAMESPACE
namespace Ui { class Map; }
QT_END_NAMESPACE

class Map : public QWidget, public Observer {
Q_OBJECT

private:
    Session *session;

public:
    explicit Map(Session *session, QWidget *parent = nullptr);

    ~Map() override;

    void update() override;

private:
    void paintEvent(QPaintEvent *event) override;

private:
    Ui::Map *ui;
};


#endif //E916_DENIS916_MAP_H
