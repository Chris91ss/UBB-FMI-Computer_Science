#include "testBill.h"
#include <cassert>

void TestBill::testAllBill() {
    testGetters();
    testSetters();
    testOperators();
}

void TestBill::testGetters() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    assert(bill1.getCompanyName() == "E-On");
    assert(bill1.getSerialNumber() == "EED36677");
    assert(bill1.getSum() == 122.00);
    assert(bill1.getIsPaid() == true);
    assert(bill2.getCompanyName() == "Orange");
    assert(bill2.getSerialNumber() == "X990TTRR");
    assert(bill2.getSum() == 46.00);
    assert(bill2.getIsPaid() == true);
}

void TestBill::testSetters() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    bill1.setSerialNumber("1234RR55");
    bill1.setSum(23.00);
    bill1.setIsPaid(false);
    bill2.setSerialNumber("TRE3EERR");
    bill2.setSum(10.00);
    bill2.setIsPaid(true);
    assert(bill1.getSerialNumber() == "1234RR55");
    assert(bill1.getSum() == 23.00);
    assert(bill1.getIsPaid() == false);
    assert(bill2.getSerialNumber() == "TRE3EERR");
    assert(bill2.getSum() == 10.00);
    assert(bill2.getIsPaid() == true);
}

void TestBill::testOperators() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    Bill bill3 = Bill("E-On", "EED36677", 122.00, true);
    assert(bill1 == bill3);
    bill1 = bill2;
    assert(bill1.getSerialNumber() == "X990TTRR");
    assert(bill1.getSum() == 46.00);
    assert(bill1.getIsPaid() == true);
}

