//
// Created by Adrian Trill on 21.06.2024.
//

// You may need to build the project (run Qt uic code generator) to get "ui_gui.h" resolved

#include "gui.h"
#include "ui_gui.h"
#include <QMessageBox>


gui::gui(QWidget *parent, Service *service, Participant *participant) :
        QWidget(parent), ui(new Ui::gui), service(service), participant(participant){
    ui->setupUi(this);
    service->registerObserver(this);

    if(participant != nullptr) {
        this->setWindowTitle(
                QString::fromStdString(this->participant->getName() + " - " + to_string(participant->getScore())));
        updateListParticipant();
    }
    else {
        this->setWindowTitle("Presenter");
        updateListPresenter();
    }
    connect(ui->addButton, &QPushButton::clicked, this, &gui::addQuestion);
}

gui::~gui() {
    delete ui;
}


void gui::updateListPresenter() {
    ui->listWidget->clear();
    vector<Question *> questions = this->service->getSortedById();
    for (auto &question : questions) {
        QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(question->toString()));
        ui->listWidget->addItem(item);
    }
}

void gui::updateListParticipant() {
    ui->listWidget->clear();
    vector<Question *> questions = this->service->getSortedByScore();
    for (auto &question : questions) {
        QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(question->toStringParticipant()));
        ui->listWidget->addItem(item);
    }
}

void gui::addQuestion() {
    int id = ui->idLineEdit->text().toInt();
    string text = ui->questionLineEdit->text().toStdString();
    string correctAnswer = ui->answerLineEdit->text().toStdString();

    if (text.empty() || correctAnswer.empty() || id == 0) {
        QMessageBox::critical(this, "Error", "Invalid input");
        return;
    }
    try {
        this->service->addQuestion(new Question(id, text, correctAnswer, 10));
    }
    catch (exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
    updateListPresenter();
}

void gui::update() {
    if(participant != nullptr) {
        updateListParticipant();
    }
    else {
        updateListPresenter();
    }
}


