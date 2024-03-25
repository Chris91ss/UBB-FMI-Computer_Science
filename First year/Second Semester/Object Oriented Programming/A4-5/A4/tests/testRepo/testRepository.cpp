#include "testRepository.h"

void TestRepository::testAllRepository() {
    testRepositoryConstructors();
    testRepositoryAdd();
    testRepositoryRemove();
    testRepositorySize();
    testRepositoryGetAll();
    testRepositorySearch();
}

void TestRepository::testRepositoryConstructors() {
    Repository<TrenchCoat> repository;
    assert(repository.GetSize() == 0);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 0);

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
    Repository<TrenchCoat> repository1(repository);
    assert(repository1.GetSize() == 5);
    assert(repository1.GetAll().GetSizeOfDynamicVector() == 5);
}

void TestRepository::testRepositoryAdd() {
    Repository<TrenchCoat> repository;
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
    assert(repository.GetAll().GetSizeOfDynamicVector() == 5);
}

void TestRepository::testRepositoryRemove() {
    Repository<TrenchCoat> repository;
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
    assert(repository.GetAll().GetSizeOfDynamicVector() == 4);
    repository.Remove(1);
    assert(repository.GetSize() == 3);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 3);
    repository.Remove(2);
    assert(repository.GetSize() == 2);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 2);
    repository.Remove(1);
    assert(repository.GetSize() == 1);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 1);
    repository.Remove(0);
    assert(repository.GetSize() == 0);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 0);
}

void TestRepository::testRepositorySize() {
    Repository<TrenchCoat> repository;
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
    assert(repository.GetAll().GetSizeOfDynamicVector() == 5);
    repository.Remove(0);
    assert(repository.GetSize() == 4);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 4);
    repository.Remove(1);
    assert(repository.GetSize() == 3);
    assert(repository.GetAll().GetSizeOfDynamicVector() == 3);
}

void TestRepository::testRepositoryGetAll() {
    Repository<TrenchCoat> repository;
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
    DynamicVector<TrenchCoat> dynamicVector = repository.GetAll();
    assert(dynamicVector.GetSizeOfDynamicVector() == 5);
    assert(dynamicVector[0] == trenchCoat1);
    assert(dynamicVector[1] == trenchCoat2);
    assert(dynamicVector[2] == trenchCoat3);
    assert(dynamicVector[3] == trenchCoat4);
    assert(dynamicVector[4] == trenchCoat5);
}

void TestRepository::testRepositorySearch() {
    Repository<TrenchCoat> repository;
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
