#pragma once
#include <string>
using namespace std;


class Bill {
private:
    string companyName;
    string serialNumber;
    double sum;
    bool isPaid;

public:
    Bill(const string& companyName, const string& serialNumber, double sum, bool isPaid);
    string ToString() const;
    string GetCompanyName() const;
    string GetSerialNumber() const;
    double GetSum() const;
    bool GetIsPaid() const;
};
