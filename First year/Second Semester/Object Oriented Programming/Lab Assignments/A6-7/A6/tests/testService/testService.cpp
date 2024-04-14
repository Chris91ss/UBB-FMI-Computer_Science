#include "testService.h"

void TestService::testAllService() {
    testServiceConstructors();
    testServiceOperator();
    testGenerateEntities();
    testServiceAdd();
    testServiceRemove();
    testServiceUpdate();
    testServiceSearch();
    testServiceGetAll();
    testServiceGetAllFiltered();
    testGetSetTotalBasketPrice();
}

void TestService::testServiceConstructors() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 1);
}

void TestService::testServiceOperator() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    Repository repository1;
    Service service1(repository1);
    service1 = service;
    assert(service1.getAllTrenchCoats().size() == 1);
}

void TestService::testGenerateEntities() {
    Repository repository;
    Service service(repository);
    service.Generate10Entities();
    assert(service.getAllTrenchCoats().size() == 10);
}

void TestService::testServiceAdd() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 1);
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 2);
}

void TestService::testServiceRemove() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 1);
    service.removeTrenchCoat("M", "red");
    assert(service.getAllTrenchCoats().empty());
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    service.removeTrenchCoat("M", "red");
    assert(service.getAllTrenchCoats().size() == 1);
}

void TestService::testServiceUpdate() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 1);
    service.updateTrenchCoat("M", "red", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 1);
}

void TestService::testServiceSearch() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    assert(service.searchTrenchCoat(TrenchCoat("M", "red", 100, 10, "https://www.google.com")));
    assert(!service.searchTrenchCoat(TrenchCoat("L", "blue", 200, 20, "https://www.google.com")));
}

void TestService::testServiceGetAll() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    assert(service.getAllTrenchCoats().size() == 2);
}

void TestService::testServiceGetAllFiltered() {
    Repository repository;
    Service service(repository);
    service.addTrenchCoat("M", "red", 100, 10, "https://www.google.com");
    service.addTrenchCoat("L", "blue", 200, 20, "https://www.google.com");
    assert(service.getFilteredBySizeTrenchCoats("M").size() == 1);
    assert(service.getFilteredBySizeTrenchCoats("L").size() == 1);
    assert(service.getFilteredBySizeTrenchCoats("S").empty());
}

void TestService::testGetSetTotalBasketPrice() {
    Repository repository;
    Service service(repository);
    service.setTotalBasketPrice(100);
    assert(service.getTotalBasketPrice() == 100);
    service.setTotalBasketPrice(200);
    assert(service.getTotalBasketPrice() == 200);
}

