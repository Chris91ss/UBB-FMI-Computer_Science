//
// Created by qdeni on 6/27/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_Map.h" resolved

#include <QPainter>
#include "../header_files/map.h"
#include "../form_files/ui_Map.h"

using namespace std;


Map::Map(Controller &controller, QWidget *parent) :
        QWidget(parent), ui(new Ui::Map), controller(controller) {
    this->controller.registerObserver(this);
    this->setWindowTitle("Map");
    this->setFixedSize(500, 500);
    this->ui->setupUi(this);
}

Map::~Map() {
    this->controller.unregisterObserver(this);
    delete this->ui;
}

void Map::update() {
    this->setVisible(false);
    this->setVisible(true);
}

void Map::paintEvent(QPaintEvent *event) {
    QPainter painter(this);

    int minLatitude = INT_MAX;
    int minLongitude = INT_MAX;
    for (const auto &report : this->controller.getReports()) {
        if (report.getLocation().first < minLatitude) {
            minLatitude = report.getLocation().first;
        }
        if (report.getLocation().second < minLongitude) {
            minLongitude = report.getLocation().second;
        }
    }

    painter.setBrush(Qt::blue);
    for (const auto &report : this->controller.getReports()) {
        int x = report.getLocation().first + abs(minLatitude) + 2;
        int y = report.getLocation().second + abs(minLongitude) + 2;

        painter.drawEllipse(x * 10, y * 10, 10, 10);
        painter.drawText(x * 10, y * 10, report.getDescription().c_str());
    }
}
