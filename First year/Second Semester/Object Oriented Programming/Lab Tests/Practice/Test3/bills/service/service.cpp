#include "service.h"

Service::Service(Repository *repository) {
    this->repository = repository;
}

void Service::AddBill(Bill *bill) const {
    this->repository->AddBill(bill);
}

vector<Bill *> Service::GetBills() const {
    return this->repository->GetBills();
}

vector<Bill *> Service::GetBillsSortedCompany() const {
    vector<Bill *> sortedBills = this->repository->GetBills();

    for (int i = 0; i < sortedBills.size(); i++) {
        for (int j = i + 1; j < sortedBills.size(); j++) {
            if (sortedBills[i]->GetCompanyName() > sortedBills[j]->GetCompanyName()) {
                Bill *aux = sortedBills[i];
                sortedBills[i] = sortedBills[j];
                sortedBills[j] = aux;
            }
        }
    }

    return sortedBills;
}

void Service::readFromFile(const string &fileName) const {
    string companyName;
    string serialNumber;
    double sum;
    string isPaidStr;
    bool isPaid;

    ifstream file(fileName);

    if(!file.is_open())
        throw runtime_error("File could not be opened!");

    while (getline(file, companyName, ';')) {
        getline(file, serialNumber, ';');
        file >> sum;
        file.ignore();
        file >> isPaidStr;
        file.ignore();

        if (isPaidStr == "true") {
            isPaid = true;
        } else {
            isPaid = false;
        }

        Bill *bill = new Bill(companyName, serialNumber, sum, isPaid);
        this->AddBill(bill);
    }

    file.close();
}

void Service::writeToFile(const string &fileName, const Bill *bill) {
    ofstream file(fileName, ios::app);

    if(!file.is_open())
        throw runtime_error("File could not be opened!");

    file << "\n";
    file << bill->GetCompanyName() << ";";
    file << bill->GetSerialNumber() << ";";
    file << bill->GetSum() << ";";
    file << bill->GetIsPaid();

    file.close();
}


