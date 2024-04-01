#include "service/service.h"

Service::Service(Repository <Bill> &repository) {
    this->repository = repository;
}

Service::Service(const Service &other) {
    this->repository = other.repository;
}

Service::~Service() = default;

void Service::addBill(const Bill &bill) {
    if(this->repository.searchElement(bill)) {
        throw runtime_error("Bill already exists!");
    }
    this->repository.addElement(bill);
}

void Service::removeBill(const string& serialNumber) {
    for(int i = 0; i < this->repository.getSize(); i++) {
        if(this->repository[i].getSerialNumber() == serialNumber) {
            this->repository.removeElement(i);
            return;
        }
    }
    throw runtime_error("Bill does not exist!");
}

void Service::Generate5Bills() {
    this->addBill(Bill("0A33455X", "Digi Sport", DateTime(15,4,2016), 75.00, false));
    this->addBill(Bill("EED36677", "E-ON", DateTime(16,3,2016), 122.00, true));
    this->addBill(Bill("AAB12345", "RCS-RDS", DateTime(17,2,2016), 45.00, false));
    this->addBill(Bill("XZC98765", "Vodafone", DateTime(18,1,2016), 30.00, true));
    this->addBill(Bill("QWE45678", "Orange", DateTime(19,12,2016), 50.00, false));
}

DynamicVector<Bill> Service::getAllBills() const {
    return this->repository.getAll();
}

DynamicVector<Bill> Service::sortAllUnpaidBillsByDueDate() const {
    DynamicVector<Bill> bills = this->repository.getAll();
    DynamicVector<Bill> filteredBills;
    for(int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        if(!bills[i].getIsPaid()) {
            filteredBills.AddToDynamicVector(bills[i]);
        }
    }

    for(int i = 0; i < filteredBills.GetSizeOfDynamicVector() - 1; i++) {
        for(int j = i + 1; j < filteredBills.GetSizeOfDynamicVector(); j++) {
            DateTime date1 = filteredBills[i].getDueDate();
            DateTime date2 = filteredBills[j].getDueDate();
            if(date1.day > date2.day || date1.month > date2.month || date1.year > date2.year) {
                Bill aux = filteredBills[i];
                filteredBills[i] = filteredBills[j];
                filteredBills[j] = aux;
            }
        }
    }

    return filteredBills;
}

double Service::calculateTotalAmountOfUnpaidBills() const {
    DynamicVector<Bill> bills = this->repository.getAll();
    DynamicVector<Bill> filteredBills;
    for(int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        if(!bills[i].getIsPaid()) {
            filteredBills.AddToDynamicVector(bills[i]);
        }
    }

    double totalAmount = 0;
    for(int i = 0; i < filteredBills.GetSizeOfDynamicVector(); i++) {
        totalAmount += filteredBills[i].getSum();
    }

    return totalAmount;
}
