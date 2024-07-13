//
// Created by qdeni on 6/28/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_CompanyGui.h" resolved

#include <QMessageBox>
#include "../header_files/companygui.h"
#include "../form_files/ui_CompanyGui.h"

using namespace std;

CompanyGui::CompanyGui(Session *session, QWidget *parent) :
        QWidget(parent), ui(new Ui::CompanyGui), session(session) {
    this->ui->setupUi(this);
    this->session->registerObserver(this);
    this->setWindowTitle(QString::fromStdString("Courier Company"));
    this->makeConnections();
    this->update();
}

CompanyGui::~CompanyGui() {
    this->session->unregisterObserver(this);
    delete this->ui;
}

void CompanyGui::update() {
    this->ui->packagesList->clear();
    for (auto &package : this->session->getPackages()) {
        this->ui->packagesList->addItem(QString::fromStdString(package.toString()));
        if (package.getStatus()) {
            this->ui->packagesList->item(this->ui->packagesList->count() - 1)->setBackground(Qt::green);
        }
    }
}

void CompanyGui::makeConnections() {
    QWidget::connect(this->ui->addButton, &QPushButton::clicked, this, &CompanyGui::addPackage);
}

void CompanyGui::addPackage() {
    try {
        string recipient = this->ui->recipientLine->text().toStdString();
        string street = this->ui->streetLine->text().toStdString();
        if (this->ui->numberLine->text().isEmpty() || this->ui->xLine->text().isEmpty() || this->ui->yLine->text().isEmpty()) {
            throw runtime_error("Invalid package data!");
        }

        int number = this->ui->numberLine->text().toInt();
        int x = this->ui->xLine->text().toInt();
        int y = this->ui->yLine->text().toInt();

        this->session->addPackage(recipient, street, number, x, y);
    } catch (const exception &error) {
        QMessageBox::warning(this, "Error", QString::fromStdString(error.what()));
    }

    this->ui->recipientLine->clear();
    this->ui->streetLine->clear();
    this->ui->numberLine->clear();
    this->ui->xLine->clear();
    this->ui->yLine->clear();
}
