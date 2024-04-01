#include <assert.h>
#include <string.h>
#include "testEstate.h"
#include "../../headers/domain/estate.h"

void TestEstate()
{
    TestCreateEstate();
    TestDestroyEstate();
    TestCopyEstate();
    TestGetEstateType();
    TestGetEstateAddress();
    TestGetEstateSurface();
    TestGetEstatePrice();
    TestSetEstateType();
    TestSetEstateSurface();
    TestSetEstatePrice();
    TestCompareEstateSurfaceAscending();
    TestCompareEstateSurfaceDescending();
}

void TestCreateEstate()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    assert((GetEstateType(estate), 0) == 0);
    assert(strcmp(GetEstateAddress(estate), "address") == 0);
    assert(GetEstateSurface(estate) == 100);
    assert(GetEstatePrice(estate) == 1000);
    DestroyEstate(estate);
}

void TestDestroyEstate()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    DestroyEstate(estate);
}

void TestCopyEstate()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    Estate* copy = CopyEstate(estate);
    assert((GetEstateType(copy), 0) == 0);
    assert(strcmp(GetEstateAddress(copy), "address") == 0);
    assert(GetEstateSurface(copy) == 100);
    assert(GetEstatePrice(copy) == 1000);
    DestroyEstate(estate);
    DestroyEstate(copy);
}

void TestGetEstateType()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    assert((GetEstateType(estate), 0) == 0);
    DestroyEstate(estate);
}

void TestGetEstateAddress()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    assert(strcmp(GetEstateAddress(estate), "address") == 0);
    DestroyEstate(estate);
}

void TestGetEstateSurface()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    assert(GetEstateSurface(estate) == 100);
    DestroyEstate(estate);
}

void TestGetEstatePrice()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    assert(GetEstatePrice(estate) == 1000);
    DestroyEstate(estate);
}

void TestSetEstateType()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    SetEstateType(estate, 1);
    assert((GetEstateType(estate), 1) == 1);
    DestroyEstate(estate);
}

void TestSetEstateSurface()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    SetEstateSurface(estate, 200);
    assert(GetEstateSurface(estate) == 200);
    DestroyEstate(estate);
}

void TestSetEstatePrice()
{
    Estate* estate = CreateEstate(0, "address", 100, 1000);
    SetEstatePrice(estate, 2000);
    assert(GetEstatePrice(estate) == 2000);
    DestroyEstate(estate);
}

void TestCompareEstateSurfaceAscending()
{
    Estate* estate1 = CreateEstate(0, "address", 100, 1000);
    Estate* estate2 = CreateEstate(0, "address", 200, 2000);
    assert(CompareEstateSurfaceAscending(estate1, estate2) == 0);
    DestroyEstate(estate1);
    DestroyEstate(estate2);
}

void TestCompareEstateSurfaceDescending()
{
    Estate* estate1 = CreateEstate(0, "address", 100, 1000);
    Estate* estate2 = CreateEstate(0, "address", 200, 2000);
    assert(CompareEstateSurfaceDescending(estate1, estate2) == 1);
    DestroyEstate(estate1);
    DestroyEstate(estate2);
}