#pragma once
#include <../../../domain/bill.h>
#include <vector>

class Repository {
private:
    vector<Bill*> bills;

public:
    Repository() = default;
    ~Repository() = default;
    void AddBill(Bill* bill);
    vector<Bill *> GetBills();
};
