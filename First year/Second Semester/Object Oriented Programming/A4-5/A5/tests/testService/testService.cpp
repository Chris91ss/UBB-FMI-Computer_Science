#include "testService.h"

void TestService::testAllService() {
    testServiceConstructors();
    testServiceOperator();
    testServiceAdd();
    testServiceRemove();
    testServiceUpdate();
    testServiceGetAll();
}

void TestService::testServiceConstructors() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
}

void TestService::testServiceOperator() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    Repository<TrenchCoat> repository1;
    Service service1(repository1);
    service1 = service;
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
}

void TestService::testServiceAdd() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 2);
}

void TestService::testServiceRemove() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
    service.removeTrenchCoat("M", "red");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 0);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    service.removeTrenchCoat("M", "red");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
}

void TestService::testServiceUpdate() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
    service.updateTrenchCoat("M", "red", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 1);
}

void TestService::testServiceGetAll() {
    Repository<TrenchCoat> repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().GetSizeOfDynamicVector() == 2);
}
