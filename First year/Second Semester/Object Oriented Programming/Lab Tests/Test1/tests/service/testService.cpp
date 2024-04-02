#include "testService.h"
#include "service/service.h"
#include <cassert>

void TestService::testAllService() {
    testAddBill();
}

void TestService::testAddBill() {
    Repository<Bill> repository;
    Service service(repository);
    Bill bill1 = Bill("E-On", "EED36677", 122.00, true);
    service.addBill(bill1);
}

void TestService::testPaidBills() {
    Repository<Bill> repository;
    Service service(repository);
    service.Generate5BillsAtStartup();
    double sum = 0;
    DynamicVector<Bill> paidBills = service.getAllPaidBillsAndTheirSum(sum);
    assert(paidBills.GetSizeOfDynamicVector() == 3);
    assert(sum == 248);
}


