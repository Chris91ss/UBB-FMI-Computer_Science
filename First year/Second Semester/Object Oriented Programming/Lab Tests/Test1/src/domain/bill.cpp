
#include "bill.h"

Bill::Bill() : companyName(""), serialNumber(""), sum(0), isPaid(false) {
}

Bill::Bill(const string &companyName, const string &serialNumber, double sum, bool isPaid) {
    this->companyName = companyName;
    this->serialNumber = serialNumber;
    this->sum = sum;
    this->isPaid = isPaid;
}

Bill::Bill(const Bill &other) {
    this->companyName = other.companyName;
    this->serialNumber = other.serialNumber;
    this->sum = other.sum;
    this->isPaid = other.isPaid;
}

Bill::~Bill() = default;

string Bill::getCompanyName() const {
    return this->companyName;
}

string Bill::getSerialNumber() const {
    return this->serialNumber;
}

double Bill::getSum() const {
    return this->sum;
}

bool Bill::getIsPaid() const {
    return this->isPaid;
}

void Bill::setSerialNumber(const string &newSerialNumber) {
    this->serialNumber = newSerialNumber;
}

void Bill::setSum(double newSum) {
    this->sum = newSum;
}

void Bill::setIsPaid(bool newIsPaid) {
    this->isPaid = newIsPaid;
}

Bill &Bill::operator=(const Bill &other) {
    this->companyName = other.companyName;
    this->serialNumber = other.serialNumber;
    this->sum = other.sum;
    this->isPaid = other.isPaid;
    return *this;
}

bool Bill::operator==(const Bill &other) {
    return this->companyName == other.companyName;
}
