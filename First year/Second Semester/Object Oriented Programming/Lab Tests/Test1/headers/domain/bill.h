#pragma once
#include <string>
using namespace std;

class Bill{
private:
    string companyName;
    string serialNumber;
    double sum;
    bool isPaid;
public:
    Bill();
    Bill(const string &companyName, const string &serialNumber, double sum, bool isPaid);
    Bill(const Bill &other);
    ~Bill();

    string getCompanyName() const;
    string getSerialNumber() const;
    double getSum() const;
    bool getIsPaid() const;

    void setSerialNumber(const string &newSerialNumber);
    void setSum(double newSum);
    void setIsPaid(bool newIsPaid);

    Bill &operator=(const Bill &other);
    bool operator==(const Bill &other);
};