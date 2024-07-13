//
// Created by qdeni on 6/25/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_DepartmentGui.h" resolved

#include <QMessageBox>
#include "../header_files/departmentgui.h"
#include "../form_files/ui_DepartmentGui.h"
#include "../header_files/utils.h"

using namespace std;


DepartmentGui::DepartmentGui(QWidget *parent) :
        QWidget(parent), ui(new Ui::DepartmentGui), controller(nullptr), department(nullptr) {
    this->ui->setupUi(this);
    this->makeConnections();
}

DepartmentGui::~DepartmentGui() {
    this->controller->unregisterObserver(this);

    delete this->ui;
}

void DepartmentGui::makeConnections() {
    QWidget::connect(this->ui->addButton, &QPushButton::clicked, this, &DepartmentGui::addVolunteer);
    QWidget::connect(this->ui->suitableButton, &QPushButton::clicked, this, &DepartmentGui::showSuitable);
    QWidget::connect(this->ui->unassignedButton, &QPushButton::clicked, this, &DepartmentGui::updateUnassignedList);
    QWidget::connect(this->ui->assignButton, &QPushButton::clicked, this, &DepartmentGui::assignVolunteer);
}

void DepartmentGui::init(Controller *controller, Department *department) {
    this->controller = controller;
    this->department = department;

    this->controller->registerObserver(this);

    this->setWindowTitle(QString::fromStdString(department->getName()));
    this->ui->descriptionLabel->setText(QString::fromStdString(department->getDescription()));
    this->update();
}

void DepartmentGui::update() {
    this->updateVolunteersList();
    this->updateUnassignedList();
}

void DepartmentGui::updateVolunteersList() {
    vector<Volunteer> departmentVolunteers;
    for (const auto& volunteer : this->controller->getVolunteers()) {
        if (volunteer.getDepartment() == this->department) {
            departmentVolunteers.push_back(volunteer);
        }
    }

    std::sort(departmentVolunteers.begin(), departmentVolunteers.end(), [](const Volunteer& a, const Volunteer& b) {
        return a.getName() < b.getName();
    });
    this->ui->volunteersList->clear();
    for (const auto& volunteer : departmentVolunteers) {
        this->ui->volunteersList->addItem(QString::fromStdString(volunteer.toString()));
    }
}

void DepartmentGui::updateUnassignedList() {
    vector<Volunteer> unassignedVolunteers;
    for (const auto& volunteer : this->controller->getVolunteers()) {
        if (volunteer.getDepartment() == nullptr) {
            unassignedVolunteers.push_back(volunteer);
        }
    }

    std::sort(unassignedVolunteers.begin(), unassignedVolunteers.end(), [](const Volunteer& a, const Volunteer& b) {
        return a.getName() < b.getName();
    });
    this->ui->unassignedList->clear();
    for (const auto &volunteer : unassignedVolunteers) {
        this->ui->unassignedList->addItem(QString::fromStdString(volunteer.toString()));
    }
}

void DepartmentGui::addVolunteer() {
    string name = this->ui->nameLineEdit->text().toStdString();
    string email = this->ui->emailLineEdit->text().toStdString();
    vector<string> interests = tokenize(this->ui->interestsLineEdit->text().toStdString(), ',');

    try {
        this->controller->addVolunteer(name, email, interests);
    } catch (const exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void DepartmentGui::showSuitable() {
    vector<Volunteer> unassignedVolunteers;
    for (const auto& volunteer : this->controller->getVolunteers()) {
        if (volunteer.getDepartment() == nullptr) {
            unassignedVolunteers.push_back(volunteer);
        }
    }

    sort(unassignedVolunteers.begin(), unassignedVolunteers.end(), [this](const Volunteer& a, const Volunteer& b) {
        int scoreA = 0, scoreB = 0;

        for (const auto& interest : a.getInterests()) {
            if (strstr(this->department->getDescription().c_str(), interest.c_str())) {
                scoreA++;
            }
        }
        for (const auto& interest : b.getInterests()) {
            if (strstr(this->department->getDescription().c_str(), interest.c_str())) {
                scoreB++;
            }
        }

        return scoreA > scoreB;
    });

    this->ui->unassignedList->clear();
    int count = 0;
    for (auto &volunteer : unassignedVolunteers) {
        if (count == 3) {
            break;
        }
        this->ui->unassignedList->addItem(QString::fromStdString(volunteer.toString()));
        count++;
    }
}

void DepartmentGui::assignVolunteer() {
    auto selectedVolunteer = this->ui->unassignedList->selectedItems()[0];
    if (selectedVolunteer == nullptr) {
        return;
    }
    string volunteerString = selectedVolunteer->text().toStdString();
    vector<string> volunteerTokens = tokenize(volunteerString, ',');

    this->controller->assignVolunteer(volunteerTokens[0], volunteerTokens[1], this->department);
}
