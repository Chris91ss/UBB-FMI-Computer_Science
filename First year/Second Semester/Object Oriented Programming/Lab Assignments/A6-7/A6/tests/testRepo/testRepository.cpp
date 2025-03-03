#include "testRepository.h"

void TestRepository::testAllRepository() {
    testRepositoryConstructors();
    testRepositoryAdd();
    testRepositoryRemove();
    testRepositorySize();
    testRepositoryGetAll();
    testRepositorySearch();
    testRepositoryBasket();
}

void TestRepository::testRepositoryConstructors() {
    Repository repository;
    assert(repository.GetSize() == 0);
    assert(repository.GetAll().empty());

    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    Repository repository1(repository);
    assert(repository1.GetSize() == 5);
    assert(repository1.GetAll().size() == 5);
}

void TestRepository::testRepositoryAdd() {
    Repository repository;
    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    assert(repository.GetSize() == 5);
    assert(repository.GetAll().size() == 5);
}

void TestRepository::testRepositoryRemove() {
    Repository repository;
    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    repository.Remove(0);
    assert(repository.GetSize() == 4);
    assert(repository.GetAll().size() == 4);
    repository.Remove(1);
    assert(repository.GetSize() == 3);
    assert(repository.GetAll().size() == 3);
    repository.Remove(2);
    assert(repository.GetSize() == 2);
    assert(repository.GetAll().size() == 2);
    repository.Remove(1);
    assert(repository.GetSize() == 1);
    assert(repository.GetAll().size() == 1);
    repository.Remove(0);
    assert(repository.GetSize() == 0);
    assert(repository.GetAll().empty());
}

void TestRepository::testRepositorySize() {
    Repository repository;
    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    assert(repository.GetSize() == 5);
    assert(repository.GetAll().size() == 5);
    repository.Remove(0);
    assert(repository.GetSize() == 4);
    assert(repository.GetAll().size() == 4);
    repository.Remove(1);
    assert(repository.GetSize() == 3);
    assert(repository.GetAll().size() == 3);
}

void TestRepository::testRepositoryGetAll() {
    Repository repository;
    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    vector<TrenchCoat> dynamicVector = repository.GetAll();
    assert(dynamicVector.size() == 5);
    assert(dynamicVector[0] == trenchCoat1);
    assert(dynamicVector[1] == trenchCoat2);
    assert(dynamicVector[2] == trenchCoat3);
    assert(dynamicVector[3] == trenchCoat4);
    assert(dynamicVector[4] == trenchCoat5);
}

void TestRepository::testRepositorySearch() {
    Repository repository;
    TrenchCoat trenchCoat1("M", "red", 100, 10, "link1");
    TrenchCoat trenchCoat2("L", "blue", 200, 20, "link2");
    TrenchCoat trenchCoat3("S", "green", 300, 30, "link3");
    TrenchCoat trenchCoat4("XL", "yellow", 400, 40, "link4");
    TrenchCoat trenchCoat5("XXL", "black", 500, 50, "link5");
    repository.Add(trenchCoat1);
    repository.Add(trenchCoat2);
    repository.Add(trenchCoat3);
    repository.Add(trenchCoat4);
    repository.Add(trenchCoat5);
    assert(repository.Search(trenchCoat1) == true);
    assert(repository.Search(trenchCoat2) == true);
    assert(repository.Search(trenchCoat3) == true);
    assert(repository.Search(trenchCoat4) == true);
    assert(repository.Search(trenchCoat5) == true);
    TrenchCoat trenchCoat6("XXL", "white", 600, 60, "link6");
    assert(repository.Search(trenchCoat6) == false);

}

void TestRepository::testRepositoryBasket() {
    Repository repository;
    repository.SetTotalBasketPrice(200);
    assert(repository.GetTotalBasketPrice() == 200);
    assert(repository.GetTotalBasketPrice() == 200);
    repository.SetTotalBasketPrice(300);
    assert(repository.GetTotalBasketPrice() == 300);
    assert(repository.GetTotalBasketPrice() == 300);
    repository.SetTotalBasketPrice(400);
    assert(repository.GetTotalBasketPrice() == 400);
    assert(repository.GetTotalBasketPrice() == 400);
}