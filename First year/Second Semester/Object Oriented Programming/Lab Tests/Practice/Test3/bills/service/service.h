#pragma once
#include "../repository/repository.h"
#include <fstream>

class Service {
private:
    Repository *repository;

public:
    Service() : repository(new Repository()) {}
    explicit Service(Repository *repository);
    ~Service() = default;
    void AddBill(Bill *bill) const;
    vector<Bill *> GetBills() const;
    vector<Bill *> GetBillsSortedCompany() const;
    void readFromFile(const string& fileName) const;
    static void writeToFile(const string& fileName, const Bill *bill);
};
