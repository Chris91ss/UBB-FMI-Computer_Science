#include "service/service.h"

Service::Service(Repository <Bill> &repository) {
    this->repository = repository;
}

Service::Service(const Service &other) {
    this->repository = other.repository;
}

Service::~Service() = default;

void Service::addBill(const Bill &bill) {
    if(this->repository.searchElementInRepository(bill))
        throw runtime_error("Bill already exists!");
    this->repository.addElementToRepository(bill);
}

void Service::Generate5BillsAtStartup() {
    this->addBill(Bill("E-On", "EED36677", 122.00, true));
    this->addBill(Bill("Orange", "X990TTRR", 46.00, true));
    this->addBill(Bill("Vodafone", "1234RR55", 23.00, false));
    this->addBill(Bill("Tcomm", "TRE3EERR", 10.00, true));
    this->addBill(Bill("Digi Sport", "0A33455X", 75.00, false));
}

DynamicVector<Bill> Service::getAllBills() const {
    return this->repository.getAllElementsFromRepository();
}

DynamicVector<Bill> Service::getAllBillsSortedByCompanyName() const {
    DynamicVector<Bill> bills = this->repository.getAllElementsFromRepository();
    for(int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        for(int j = i + 1; j < bills.GetSizeOfDynamicVector(); j++) {
            if(bills[i].getCompanyName() > bills[j].getCompanyName()) {
                Bill aux = bills[i];
                bills[i] = bills[j];
                bills[j] = aux;
            }
        }
    }

    return bills;
}

DynamicVector<Bill> Service::getAllPaidBillsAndTheirSum(double &sum) const {
    DynamicVector<Bill> bills = this->repository.getAllElementsFromRepository();
    DynamicVector<Bill> paidBills;
    sum = 0;
    for(int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        if(bills[i].getIsPaid()) {
            paidBills.AddToDynamicVector(bills[i]);
            sum += bills[i].getSum();
        }
    }

    return paidBills;
}
