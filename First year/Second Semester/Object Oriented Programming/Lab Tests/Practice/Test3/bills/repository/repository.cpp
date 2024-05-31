#include "repository.h"

void Repository::AddBill(Bill *bill) {
    this->bills.push_back(bill);
}

vector<Bill *> Repository::GetBills() {
    return this->bills;
}


