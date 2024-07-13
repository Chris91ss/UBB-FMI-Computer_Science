//
// Created by qdeni on 6/25/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_DepartmentsOverview.h" resolved

#include "../header_files/departmentsoverview.h"
#include "../form_files/ui_DepartmentsOverview.h"

using namespace std;

DepartmentsOverview::DepartmentsOverview(Controller &controller, QWidget *parent) :
        QWidget(parent), ui(new Ui::DepartmentsOverview), controller(controller) {
    ui->setupUi(this);

    this->controller.registerObserver(this);

    this->setWindowTitle("Departments Overview");
    this->updateList();
}

DepartmentsOverview::~DepartmentsOverview() {
    delete ui;
}

void DepartmentsOverview::update() {
    this->updateList();
}

void DepartmentsOverview::updateList() {
    vector<pair<string, int>> departments;
    for (const auto& department : this->controller.getDepartments()) {
        int cnt = 0;
        for (const auto& volunteer : this->controller.getVolunteers()) {
            if (volunteer.getDepartment() == &department) {
                cnt++;
            }
        }

        departments.emplace_back(department.getName(), cnt);
    }

    std::sort(departments.begin(), departments.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        return a.second > b.second;
    });

    this->ui->departmentsList->clear();
    for (const auto& department : departments) {
        string departmentString = department.first + " - " + to_string(department.second) + " volunteers";
        this->ui->departmentsList->addItem(QString::fromStdString(departmentString));
    }
}
