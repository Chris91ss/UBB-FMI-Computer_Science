//
// Created by qdeni on 6/26/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_StatisticGui.h" resolved

#include <QPainter>
#include "../header_files/statisticgui.h"
#include "../form_files/ui_StatisticGui.h"

using namespace std;

StatisticGui::StatisticGui(Controller &controller, QWidget *parent) :
        QWidget(parent), ui(new Ui::StatisticGui), controller(controller) {
    this->ui->setupUi(this);
    this->controller.registerObserver(this);
    this->setWindowTitle("Statistics");
    this->setFixedSize(500, 500);
    this->show();
}

StatisticGui::~StatisticGui() {
    delete this->ui;
}

void StatisticGui::update() {
    this->setVisible(false);
    this->setVisible(true);
}

void StatisticGui::paintEvent(QPaintEvent *event) {
    vector<pair<string, int>> data;
    for (const auto &patient : this->controller.getPatients()) {
        bool found = false;
        for (auto &p : data) {
            if (p.first == patient.getSpecialization()) {
                p.second++;
                found = true;
                break;
            }
        }

        if (!found) {
            data.emplace_back(patient.getSpecialization(), 1);
        }
    }

    QPainter painter(this);
    QRectF size = QRectF(0, 0, this->width(), this->height());

    int i = 0;
    for (const auto &specialization : data) {
        /// math to compute the size of each slice
        int sliceSize = specialization.second * 360 / this->controller.getPatients().size();
        /// this is to get another color for each slice
        painter.setBrush(QColor::fromHsl(i % 255, 255, 127));
        /// math to compute the placement of each slice
        painter.drawPie(size, i * 16, sliceSize * 16);
        i += sliceSize;
    }
}
