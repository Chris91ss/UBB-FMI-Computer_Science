//
// Created by Chris on 6/19/2024.
//

// You may need to build the project (run Qt uic code generator) to get "ui_GUI.h" resolved

#include "gui.h"
#include "ui_GUI.h"
#include <QMessageBox>


GUI::GUI(QWidget *parent, Service *service, User *user) :
QWidget(parent), ui(new Ui::GUI), service(service), user(user) {
    ui->setupUi(this);
    service->registerObserver(this);

    this->setWindowTitle(QString::fromStdString(user->getName() + " - " + user->getType()));

    if(user->getType() != "tester") {
        ui->addButton->hide();
        ui->descriptionLineEdit->hide();
    }

    connect(ui->addButton, &QPushButton::clicked, this, &GUI::addIssue);
    connect(ui->removeButton, &QPushButton::clicked, this, &GUI::removeIssue);
    connect(ui->resolveButton, &QPushButton::clicked, this, &GUI::resolveIssue);
    connect(ui->listIssueWidget, &QListWidget::itemSelectionChanged, this, &GUI::onSelectionChanged);
    updateList();
}

GUI::~GUI() {
    delete ui;
}

void GUI::updateList() {
    ui->listIssueWidget->clearSelection();
    ui->listIssueWidget->clear();
    for (const auto &issue : service->sortByStatusAndDescription()) {
        QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(issue->toString()));
        ui->listIssueWidget->addItem(item);
    }
}

void GUI::addIssue() {
    if(ui->descriptionLineEdit->text().isEmpty()) {
        QMessageBox::warning(this, "Warning", "Description cannot be empty!");
        return;
    }

    Issue *issue = new Issue();
    issue->setDescription(ui->descriptionLineEdit->text().toStdString());
    issue->setStatus("open");
    issue->setReporterName(user->getName());
    issue->setSolverName("");
    try{
        service->addIssueToRepo(issue);
    } catch (const std::exception &e) {
        QMessageBox::warning(this, "Warning", e.what());
        return;
    }
    updateList();
}

void GUI::removeIssue() {
    // get the first selected item from the list
    QListWidgetItem *item = ui->listIssueWidget->selectedItems().at(0);
    // get the description of the issue
    std::string text = item->text().toStdString();
    std::string description = text.substr(0, text.find(";"));
    std::string status = text.substr(text.find(";") + 1, text.find(";", text.find(";") + 1) - text.find(";") - 1);
    // remove the issue from the repository
    if(status != "closed") {
        QMessageBox::warning(this, "Warning", "Issue is not closed!");
        return;
    }
    service->removeIssueFromRepo(description);
    // update the list
    updateList();
}

void GUI::resolveIssue() {
    // get the first selected item from the list
    QListWidgetItem *item = ui->listIssueWidget->selectedItems().at(0);
    // get the description of the issue
    std::string text = item->text().toStdString();
    std::string description = text.substr(0, text.find(";"));
    std::string reporter = text.substr(text.find(";", text.find(";") + 1) + 1, text.find(";", text.find(";", text.find(";") + 1) + 1) - text.find(";", text.find(";") + 1) - 1);

    service->updateIssueInRepo(description, "closed", reporter, user->getName());
    // update the list
    updateList();
}

void GUI::onSelectionChanged() {
    if(ui->listIssueWidget->selectedItems().isEmpty()) {
        ui->resolveButton->setEnabled(false);
        return;
    }

    QListWidgetItem *item = ui->listIssueWidget->selectedItems().at(0);
    std::string text = item->text().toStdString();
    std::string status = text.substr(text.find(";") + 1, text.find(";", text.find(";") + 1) - text.find(";") - 1);

    if(status == "open") {
        ui->resolveButton->setEnabled(true);
    } else {
        ui->resolveButton->setEnabled(false);
    }
}

void GUI::update() {
    updateList();
}
