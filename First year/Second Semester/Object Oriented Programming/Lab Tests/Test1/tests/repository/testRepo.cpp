#include "testRepo.h"
#include "bill.h"
#include "repository/repository.h"
#include <cassert>

void TestRepo::testAllRepo() {
    testAddBill();
    testOperators();
    testGetSize();
    testSearchBill();
}

void TestRepo::testAddBill() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    Repository<Bill> repository;
    repository.addElementToRepository(bill1);
    repository.addElementToRepository(bill2);
    assert(repository.getSizeOfRepository() == 2);
}

void TestRepo::testOperators() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    Repository<Bill> repository;
    repository.addElementToRepository(bill1);
    repository.addElementToRepository(bill2);
    assert(repository[0] == bill1);
    assert(repository[1] == bill2);
}

void TestRepo::testGetSize() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    Repository<Bill> repository;
    repository.addElementToRepository(bill1);
    repository.addElementToRepository(bill2);
    assert(repository.getSizeOfRepository() == 2);
}

void TestRepo::testSearchBill() {
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    Bill bill2 = Bill("Orange", "X990TTRR", 46.00, true);
    Repository<Bill> repository;
    repository.addElementToRepository(bill1);
    repository.addElementToRepository(bill2);
    assert(repository.searchElementInRepository(bill1) == true);
    assert(repository.searchElementInRepository(bill2) == true);
}
