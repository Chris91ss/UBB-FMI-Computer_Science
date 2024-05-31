//
// Created by Chris on 5/27/2024.
//

// You may need to build the project (run Qt uic code generator) to get "ui_GUI.h" resolved

#include "gui.h"
#include "ui_GUI.h"


GUI::GUI(QWidget *parent, Service service) : QWidget(parent), ui(new Ui::GUI), service(service) {
    ui->setupUi(this);
    populateList();

    connect(ui->showSymptomsPushButton, &QPushButton::clicked, this, &GUI::populateSymptomsList);
    connect(ui->searchLineEdit, &QLineEdit::textChanged, this, &GUI::populateSearchList);
}

GUI::~GUI() {
    delete ui;
}

void GUI::populateList() const {
    ui->listWidget->clear();
    for (const auto &bill : service.GetSortedDisorders()) {
        auto *item = new QListWidgetItem(QString::fromStdString(bill->toString()));
        ui->listWidget->addItem(item);
    }
}

void GUI::populateSymptomsList() const {
    ui->symptomsListWidget->clear();

    auto *disorderName = ui->disorderLineEdit->text().toStdString().c_str();
    bool found = service.searchDisorder(disorderName);
    if(found) {
        for (const auto &bill : service.GetDisorderSymptoms(disorderName)) {
            auto *item = new QListWidgetItem(QString::fromStdString(bill));
            ui->symptomsListWidget->addItem(item);
        }
    }
    else {
        ui->errorLineEdit->setText("No disorder found!");
    }

}

void GUI::populateSearchList() {
    ui->listWidget->clear();

    auto *search = ui->searchLineEdit->text().toStdString().c_str();

    for(auto &disorder : service.GetSortedDisorders()) {
        if(disorder->getName().find(search) != std::string::npos) {
            auto *item = new QListWidgetItem(QString::fromStdString(disorder->toString()));
            ui->listWidget->addItem(item);
        }
        else if(disorder->getCategory().find(search) != std::string::npos) {
            auto *item = new QListWidgetItem(QString::fromStdString(disorder->toString()));
            ui->listWidget->addItem(item);
        }
    }

}
