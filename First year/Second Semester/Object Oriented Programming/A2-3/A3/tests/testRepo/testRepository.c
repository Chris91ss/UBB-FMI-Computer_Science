#include <assert.h>
#include <string.h>
#include "testRepository.h"
#include "../../headers/repository/repository.h"

void TestRepository()
{
    TestCreateRepository();
    TestDestroyRepository();
    TestCopyRepository();
    TestAdd();
    TestDelete();
    TestUpdate();
    TestGetEstate();
    TestGetAll();
}

void TestCreateRepository()
{
    Repository* repository = CreateRepository();
    assert(repository->estates->length == 0);
    assert(repository->estates->capacity == 2);
    DestroyRepository(repository);
}

void TestDestroyRepository()
{
    Repository* repository = CreateRepository();
    DestroyRepository(repository);
}

void TestCopyRepository()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    Repository* copy = CopyRepository(repository);
    assert(copy->estates->length == 1);
    assert(copy->estates->capacity == 2);
    DestroyRepository(repository);
    DestroyRepository(copy);
}

void TestAdd()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    assert(repository->estates->length == 1);
    assert(repository->estates->capacity == 2);
    DestroyRepository(repository);
}

void TestDelete()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    Delete(repository, "address");
    assert(repository->estates->length == 0);
    assert(repository->estates->capacity == 2);
    DestroyRepository(repository);
}

void TestUpdate()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    Update(repository, "address", 0, 200, 20000);
    assert(repository->estates->length == 1);
    assert(repository->estates->capacity == 2);
    assert(strcmp(GetEstateAddress(repository->estates->elems[0]), "address") == 0);
    assert(GetEstateType(repository->estates->elems[0]) == 0);
    assert(GetEstateSurface(repository->estates->elems[0]) == 200);
    assert(GetEstatePrice(repository->estates->elems[0]) == 20000);
    DestroyRepository(repository);
}

void TestGetEstate()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    Estate* estateCopy = GetEstate(repository, "address");
    assert(strcmp(estateCopy->address, "address") == 0);
    assert(estateCopy->type == 0);
    assert(estateCopy->surface == 100);
    assert(estateCopy->price == 10000);
    DestroyRepository(repository);
}

void TestGetAll()
{
    Repository* repository = CreateRepository();
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    Add(repository, estate);
    DynamicArray* allEstates = GetAll(repository);
    assert(allEstates->length == 1);
    assert(allEstates->capacity == 2);
    DestroyRepository(repository);
    DestroyDynamicArray(allEstates);
}
