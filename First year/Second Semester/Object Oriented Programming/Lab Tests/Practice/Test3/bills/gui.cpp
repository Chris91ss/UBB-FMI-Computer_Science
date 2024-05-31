#include "gui.h"
#include "ui_GUI.h"


GUI::GUI(QWidget *parent, Service service) : QWidget(parent), ui(new Ui::GUI), service(service) {
    ui->setupUi(this);

    connect(ui->calculateTotalButton, &QPushButton::clicked, this, &GUI::calculateTotal);
    connect(ui->filterButton, &QPushButton::clicked, this, &GUI::filterByUnpaidOrPaid);
    connect(ui->addButton, &QPushButton::clicked, this, &GUI::addBill);
    connect(ui->showAllButton, &QPushButton::clicked, this, &GUI::populateList);

    populateList();
}

GUI::~GUI() {
    delete ui;
}

void GUI::populateList() const {
    ui->listWidget->clear();
    for (const auto &bill : service.GetBillsSortedCompany()) {
        auto *item = new QListWidgetItem(QString::fromStdString(bill->ToString()));

        if (!bill->GetIsPaid()) {
            item->setBackground(Qt::red);
        }

        ui->listWidget->addItem(item);
    }
}

void GUI::filterByUnpaidOrPaid() const {
    ui->listWidget->clear();
    if(ui->checkBox->isChecked()) {
        for(const auto &bill : service.GetBillsSortedCompany())
            if(bill->GetIsPaid())
                ui->listWidget->addItem(QString::fromStdString(bill->ToString()));
    }
    else {
        for(const auto &bill : service.GetBillsSortedCompany())
            if(!bill->GetIsPaid()) {
                auto *item = new QListWidgetItem(QString::fromStdString(bill->ToString()));
                item->setBackground(Qt::red);
                ui->listWidget->addItem(item);
            }
    }
}

void GUI::calculateTotal() const {
    auto *companyName = ui->companyLineEdit->text().toStdString().c_str();

    double total = 0;
    bool found = false;

    for(const auto &bill : service.GetBillsSortedCompany())
        if(bill->GetCompanyName() == companyName) {
            total += bill->GetSum();
            found = true;
        }

    if(found)
        ui->totalResultlineEdit->setText(QString::number(total));
    else
        ui->errorLineEdit->setText("Company not found!");
}

void GUI::addBill() const {
    try {
        auto *companyName = ui->addCompanyNameLineEdit->text().toStdString().c_str();
        auto *serialNumber = ui->addSerialNumberLineEdit->text().toStdString().c_str();
        auto sum = ui->addSumLineEdit->text().toDouble();
        auto isPaid = ui->addIsPaidCheckBox->isChecked();

        auto bill = new Bill(companyName, serialNumber, sum, isPaid);
        service.AddBill(bill);
        Service::writeToFile("../bills.txt", bill);
        populateList();
    }
    catch (std::exception &e) {
        ui->errorLineEdit->setText(e.what());
    }
}
