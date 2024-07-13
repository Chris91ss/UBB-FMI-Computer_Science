//
// Created by qdeni on 6/27/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_DriverGui.h" resolved

#include "../header_files/drivergui.h"
#include "../form_files/ui_DriverGui.h"
#include <ctime>
#include <QMessageBox>

using namespace std;

DriverGui::DriverGui(QWidget *parent) :
        QWidget(parent), ui(new Ui::DriverGui), driver(nullptr), controller(nullptr) {
    this->ui->setupUi(this);
}

DriverGui::~DriverGui() {
    this->controller->unregisterObserver(this);
    delete this->ui;
}

void DriverGui::init(Driver *driver, Controller *controller) {
    this->driver = driver;
    this->controller = controller;
    this->controller->registerObserver(this);
    this->makeConnections();
    this->update();
    this->setWindowTitle(QString::fromStdString(this->driver->getName()));
    this->show();
}

void DriverGui::makeConnections() {
    QWidget::connect(this->ui->sendButton, &QPushButton::clicked, this, &DriverGui::sendMessage);
    QWidget::connect(this->ui->addButton, &QPushButton::clicked, this, &DriverGui::addReport);
    QWidget::connect(this->ui->updateButton, &QPushButton::clicked, this, &DriverGui::validateReport);
}

void DriverGui::update() {
    auto location = this->driver->getLocation();
    this->ui->latitudeInfoLineEdit->setText(QString::number(location.first));
    this->ui->longitudeInfoLineEdit->setText(QString::number(location.second));
    this->ui->scoreInfoLineEdit->setText(QString::number(this->driver->getScore()));

    this->ui->reportsList->clear();
    for (const auto &report : this->controller->getNearbyReports(location, 10)) {
        this->ui->reportsList->addItem(QString::fromStdString(report.toString()));
        if (report.getStatus()) {
            this->ui->reportsList->item(this->ui->reportsList->count() - 1)->setFont(QFont("Times", 10, QFont::Bold));
        }
    }

    this->ui->messagesList->clear();
    for (const auto &message : this->controller->getMessages()) {
        this->ui->messagesList->addItem(QString::fromStdString(message.toString()));
    }
}

void DriverGui::sendMessage() {
    string text = this->ui->messagesLineEdit->text().toStdString();
    if (text.empty()) {
        return;
    }
    time_t now = time(nullptr);
    tm *ltm = localtime(&now);
    string time = to_string(ltm->tm_hour) + ":" + to_string(ltm->tm_min);

    this->controller->addMessage(text, this->driver->getName(), time);
    this->ui->messagesLineEdit->clear();
}

void DriverGui::addReport() {
    try {
        string description = this->ui->descriptionLineEdit->text().toStdString();
        int latitude = this->ui->latitudeLineEdit->text().toInt();
        int longitude = this->ui->longitudeLineEdit->text().toInt();

        this->controller->addReport(description, this->driver->getName(), make_pair(latitude, longitude),
                                    false, this->driver->getLocation());
    } catch (exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void DriverGui::validateReport() {
    try {
        auto selectedIndexes = this->ui->reportsList->selectionModel()->selectedIndexes();
        if (selectedIndexes.empty()) {
            throw runtime_error("No report selected!");
        }

        string selectedReport = selectedIndexes.at(0).data().toString().toStdString();
        vector<string> tokens = tokenize(selectedReport, ';');
        string description = tokens[0];
        string reporter = tokens[1];
        pair<int, int> location = make_pair(stoi(tokens[2]), stoi(tokens[3]));

        this->controller->validateReport(description, reporter, location, this->driver->getName());
    } catch (exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}
