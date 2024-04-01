#pragma once
#include "bill.h"
#include "repository/repository.h"

class Service {
private:
    Repository<Bill> repository;
public:
    Service(Repository<Bill> &repository);
    Service(const Service &other);
    ~Service();

    void addBill(const Bill &bill);
    void removeBill(const string& serialNumber);
    void Generate5Bills();
    DynamicVector<Bill> getAllBills() const;
    DynamicVector<Bill> sortAllUnpaidBillsByDueDate() const;
    double calculateTotalAmountOfUnpaidBills() const;
};