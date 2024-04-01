#pragma once
#include <string>
#include "dateTime.h"

using namespace std;

class Bill{
private:
    string serialNumber;
    string company;
    DateTime dueDate;
    double sum;
    bool isPaid;
public:
    Bill();
    Bill(const string& serialNumber, const string& company, const DateTime& dueDate, double sum, bool isPaid);
    Bill(const Bill& bill);
    ~Bill();
    Bill &operator=(const Bill &bill);
    bool operator==(const Bill &bill);

    string getSerialNumber();
    string getCompany();
    DateTime getDueDate();
    double getSum() const;
    bool getIsPaid() const;

    void setCompany(string& newCompany);
    void setDueDate(DateTime& newDueDate);
    void setSum(double newSum);
    void setIsPaid(bool newIsPaid);
};