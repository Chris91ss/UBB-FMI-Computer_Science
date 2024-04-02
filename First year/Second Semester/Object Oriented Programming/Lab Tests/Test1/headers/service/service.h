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

    /// Adds a bill to the repository
    /// \param bill - the bill to be added
    void addBill(const Bill &bill);
    void Generate5BillsAtStartup();
    DynamicVector<Bill> getAllBills() const;
    DynamicVector<Bill> getAllBillsSortedByCompanyName() const;
    /// Updates the paid status of a bill and sets it to true and passes the sum of all paid bills
    /// \param sum - the sum of all paid bills
    DynamicVector<Bill> getAllPaidBillsAndTheirSum(double &sum) const;
};