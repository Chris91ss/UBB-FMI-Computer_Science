#include "bill.h"

Bill::Bill() {
    this->serialNumber = "";
    this->company = "";
    this->dueDate.day = 0;
    this->dueDate.month = 0;
    this->dueDate.year = 0;
    this->sum = 0;
    this->isPaid = false;
}

Bill::Bill(const string& serialNumber, const string& company, const DateTime& dueDate, double sum, bool isPaid) {
    this->serialNumber = serialNumber;
    this->company = company;
    this->dueDate = dueDate;
    this->sum = sum;
    this->isPaid = isPaid;
}

Bill::Bill(const Bill &bill){
    this->serialNumber = bill.serialNumber;
    this->company = bill.company;
    this->dueDate = bill.dueDate;
    this->sum = bill.sum;
    this->isPaid = bill.isPaid;
}

Bill::~Bill() = default;

Bill &Bill::operator=(const Bill &bill) {
    this->serialNumber = bill.serialNumber;
    this->company = bill.company;
    this->dueDate = bill.dueDate;
    this->sum = bill.sum;
    this->isPaid = bill.isPaid;
    return *this;
}

bool Bill::operator==(const Bill &bill) {
    return false;
}

string Bill::getSerialNumber() {
    return this->serialNumber;
}

string Bill::getCompany() {
    return this->company;
}

DateTime Bill::getDueDate() {
    return this->dueDate;
}

double Bill::getSum() const {
    return this->sum;
}

bool Bill::getIsPaid() const {
    return this->isPaid;
}

void Bill::setCompany(string& newCompany) {
    this->company = newCompany;
}

void Bill::setDueDate(DateTime& newDueDate) {
    this->dueDate = newDueDate;
}

void Bill::setSum(double newSum) {
    this->sum = newSum;
}

void Bill::setIsPaid(bool newIsPaid) {
    this->isPaid = newIsPaid;
}
