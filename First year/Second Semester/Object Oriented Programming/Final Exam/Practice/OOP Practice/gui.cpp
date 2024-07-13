//
// Created by Adrian Trill on 20.06.2024.
//

// You may need to build the project (run Qt uic code generator) to get "ui_gui.h" resolved

#include "gui.h"
#include "ui_gui.h"
#include <QMessageBox>


gui::gui(QWidget *parent, Service *service, Person *person) : QWidget(parent), ui(new Ui::gui), service(service), person(person) {
    ui->setupUi(this);
    this->populateList();
    service->registerObserver(this);

    this->setWindowTitle(QString::fromStdString(this->person->getName() + " - " + this->person->getLongitude() + " - " + this->person->getLatitude()));

    QObject::connect(ui->checkBox, &QCheckBox::stateChanged, this, &gui::showEventsNearPerson);
    QObject::connect(ui->addButon, &QPushButton::clicked, this, &gui::addEvent);
    QObject::connect(ui->updateButton, &QPushButton::clicked, this, &gui::updateEvent);
    QObject::connect(ui->listEventsWidget, &QListWidget::itemClicked, this, &gui::eventSelected);
    QObject::connect(ui->goingButton, &QPushButton::clicked, this, &gui::onGoingButtonClicked);  // New connection

    ui->organizerControls->setVisible(false); // Ensure it is hidden by default
}



gui::~gui() {
    delete ui;
}

void gui::populateList() {
    ui->listEventsWidget->clear();
    vector<Event*> events = this->service->getEventsByDate();
    for (auto & event : events) {
        if (event->getOrganiser() == this->person->getName()) {
            QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
            item->setBackground(Qt::green);
            ui->listEventsWidget->addItem(item);
        } else {
            QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
            ui->listEventsWidget->addItem(item);
        }
    }

}

void gui::showEventsNearPerson() {
    ui->listEventsWidget->clear();
    vector<Event*> events = this->service->getEventsByDate();
    if(ui->checkBox->isChecked())
    {
        for (auto & event : events) {
            if (event->getOrganiser() == this->person->getName()) {
                QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
                item->setBackground(Qt::green);
                ui->listEventsWidget->addItem(item);
            } else {
                if (sqrt(pow(stod(event->getLatitude()) - stod(this->person->getLatitude()), 2) + pow(stod(event->getLongitude()) - stod(this->person->getLongitude()), 2)) <= 5) {
                    QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
                    ui->listEventsWidget->addItem(item);
                }
            }
        }
    }
    else
    {
        for (auto & event : events) {
            if (event->getOrganiser() == this->person->getName()) {
                QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
                item->setBackground(Qt::green);
                ui->listEventsWidget->addItem(item);
            } else {
                QListWidgetItem *item = new QListWidgetItem(QString::fromStdString(event->getName() + " - " + event->getDate() + " - " + event->getDescription()));
                ui->listEventsWidget->addItem(item);
            }
        }
    }
}


void gui::addEvent() {
    string name = ui->eventNameLineEdit->text().toStdString();
    string description = ui->eventDescriptionLineEdit->text().toStdString();
    string latitude = ui->eventLatitudeLineEdit->text().toStdString();
    string longitude = ui->eventLongitudeLineEdit->text().toStdString();
    string date = ui->eventDateLineEdit->text().toStdString();
    if(name.empty() || description.empty() || latitude.empty() || longitude.empty() || date.empty())
    {
        QMessageBox::critical(this, "Error", "All fields must be filled!");
        return;
    }
    try{
        this->service->addEvent(this->person->getName(), name, description, latitude, longitude, date);
    }
    catch (runtime_error & error) {
        QMessageBox::critical(this, "Error", error.what());
        return;
    }
    this->populateList();
}


void gui::onGoingButtonClicked() {
    QListWidgetItem *selectedItem = ui->listEventsWidget->currentItem();
    if (!selectedItem) return;

    string selectedText = selectedItem->text().toStdString();
    string selectedEventName = selectedText.substr(0, selectedText.find(" - "));

    try {
        this->service->markPersonAsGoingToEvent(this->person->getName(), selectedEventName);
        QMessageBox::information(this, "Success", "You are now marked as going to this event.");
    } catch (runtime_error &error) {
        QMessageBox::critical(this, "Error", error.what());
        return;
    }

    this->updateAttendeesList(selectedEventName);  // Update the attendees list
}

void gui::eventSelected() {
    QListWidgetItem *selectedItem = ui->listEventsWidget->currentItem();
    if (!selectedItem) return;

    string selectedText = selectedItem->text().toStdString();
    string selectedEventName = selectedText.substr(0, selectedText.find(" - "));
    Event *event = this->service->getEventByName(selectedEventName);

    if (!event) return;

    ui->eventDescriptionLabel->setText(QString::fromStdString(event->getDescription()));
    ui->eventDateLabel->setText(QString::fromStdString(event->getDate()));

    if (this->person->getName() != event->getOrganiser()) {
        ui->goingButton->setEnabled(!this->service->isPersonGoingToEvent(this->person->getName(), event->getName()));
        ui->organizerControls->setVisible(false);
    } else {
        ui->goingButton->setEnabled(false);
        ui->organizerControls->setVisible(true);
        ui->updateEventDescriptionLineEdit->setText(QString::fromStdString(event->getDescription()));
        ui->updateEventDateLineEdit->setText(QString::fromStdString(event->getDate()));
    }

    this->updateAttendeesList(selectedEventName);
}

void gui::updateAttendeesList(const string &eventName) {
    Event *event = this->service->getEventByName(eventName);
    if (!event) return;

    string attendees = "Attendees: \n";
    for (const auto &attendee : event->getAttendees()) {
        attendees += attendee + "\n";
    }
    ui->attendeesLabel->setText(QString::fromStdString(attendees));
}



void gui::updateEvent() {
    string description = ui->updateEventDescriptionLineEdit->text().toStdString();
    string date = ui->updateEventDateLineEdit->text().toStdString();
    if (description.empty() || date.empty()) {
        QMessageBox::critical(this, "Error", "Description and date cannot be empty!");
        return;
    }

    QListWidgetItem *selectedItem = ui->listEventsWidget->currentItem();
    if (!selectedItem) return;

    string selectedText = selectedItem->text().toStdString();
    string selectedEventName = selectedText.substr(0, selectedText.find(" - "));

    try {
        this->service->updateEvent(selectedEventName, description, person->getLatitude(), this->person->getLongitude(), date);
    } catch (runtime_error &error) {
        QMessageBox::critical(this, "Error", error.what());
        return;
    }
    this->populateList();
}

void gui::update() {
    this->populateList();
}
