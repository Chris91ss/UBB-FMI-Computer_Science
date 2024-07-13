//
// Created by qdeni on 6/25/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_TaskManager.h" resolved

#include <QMessageBox>
#include "../header_files/taskmanager.h"
#include "../form_files/ui_TaskManager.h"


TaskManager::TaskManager(QWidget *parent) :
        QWidget(parent), ui(new Ui::TaskManager), model(nullptr), controller(nullptr) {
    this->ui->setupUi(this);

    this->makeConnections();
}

TaskManager::~TaskManager() {
    delete this->ui;
}

void TaskManager::makeConnections() {
    QObject::connect(this->ui->addButton, &QPushButton::clicked, this, &TaskManager::addTask);
}

void TaskManager::init(QAbstractItemModel *model, Controller *controller, Programmer *programmer) {
    this->model = model;
    this->controller = controller;
    this->programmer = programmer;

    this->setWindowTitle(QString::fromStdString(this->programmer->getName()));

    this->ui->tasksTable->setModel(model);
    this->ui->tasksTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
}

void TaskManager::addTask() {
    std::string description = this->ui->descriptionLineEdit->text().toStdString();
    std::string status = this->ui->descriptionLineEdit->text().toStdString();

    try {
        this->controller->addTask(description, this->programmer->getId());
    } catch (std::exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}
