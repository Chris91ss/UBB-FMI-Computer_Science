#include "bill.h"

Bill::Bill(const string& companyName, const string& serialNumber, double sum, bool isPaid) {
    this->companyName = companyName;
    this->serialNumber = serialNumber;
    this->sum = sum;
    this->isPaid = isPaid;
}

string Bill::ToString() const {
    return companyName + " " + to_string(sum);
}

string Bill::GetCompanyName() const {
    return this->companyName;
}

string Bill::GetSerialNumber() const {
    return this->serialNumber;
}

double Bill::GetSum() const {
    return this->sum;
}

bool Bill::GetIsPaid() const {
    return this->isPaid;
}
