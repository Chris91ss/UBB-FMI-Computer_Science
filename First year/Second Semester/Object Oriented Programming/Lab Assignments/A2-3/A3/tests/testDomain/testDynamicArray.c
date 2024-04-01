#include <assert.h>
#include "testDynamicArray.h"
#include "../../headers/domain/dynamicArray.h"
#include "../../headers/domain/estate.h"

void TestDynamicArray()
{
    TestCreateDynamicArray();
    TestDestroyDynamicArray();
    TestResizeDynamicArray();
    TestAddElementToDynamicArray();
    TestRemoveElementFromDynamicArray();
    TestGetDynamicArray();
}

void TestCreateDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    assert(dynamicArray->length == 0);
    assert(dynamicArray->capacity == 2);
    assert(dynamicArray->destroyFunction == (DestroyFunction)DestroyEstate);
    DestroyDynamicArray(dynamicArray);
}

void TestDestroyDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    DestroyDynamicArray(dynamicArray);
}

void TestResizeDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    dynamicArray->capacity *= 2;
    ResizeDynamicArray(dynamicArray);
    assert(dynamicArray->capacity == 4);
    DestroyDynamicArray(dynamicArray);
}

void TestAddElementToDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    Estate *estate = CreateEstate(0, "address", 2, 3);
    AddElementToDynamicArray(dynamicArray, estate);
    assert(dynamicArray->length == 1);
    assert(dynamicArray->capacity == 2);
    assert(dynamicArray->elems[0] == estate);
    DestroyDynamicArray(dynamicArray);
}

void TestRemoveElementFromDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    Estate *estate = CreateEstate(0, "address", 2, 3);
    AddElementToDynamicArray(dynamicArray, estate);
    RemoveElementFromDynamicArray(dynamicArray, 0);
    assert(dynamicArray->length == 0);
    assert(dynamicArray->capacity == 2);
    DestroyDynamicArray(dynamicArray);
}

void TestGetDynamicArray()
{
    DynamicArray *dynamicArray = CreateDynamicArray(2, (DestroyFunction)DestroyEstate);
    Estate *estate = CreateEstate(0, "address", 2, 3);
    AddElementToDynamicArray(dynamicArray, estate);
    assert(GetDynamicArray(dynamicArray, 0) == estate);
    DestroyDynamicArray(dynamicArray);
}
