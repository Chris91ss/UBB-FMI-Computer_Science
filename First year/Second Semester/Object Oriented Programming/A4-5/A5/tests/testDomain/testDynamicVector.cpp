#include "testDynamicVector.h"

void TestDynamicVector::testAllDynamicVector() {
    testDynamicVectorConstructors();
    testDynamicVectorAdd();
    testDynamicVectorRemove();
    testDynamicVectorOperator();
    testDynamicVectorSize();
    testDynamicVectorSearch();
}

void TestDynamicVector::testDynamicVectorConstructors() {
    DynamicVector<int> dynamicVector;
    assert(dynamicVector.GetSizeOfDynamicVector() == 0);

    dynamicVector.AddToDynamicVector(1);
    DynamicVector<int> dynamicVector1(dynamicVector);
    assert(dynamicVector1.GetSizeOfDynamicVector() == 1);
}

void TestDynamicVector::testDynamicVectorAdd() {
    DynamicVector<int> dynamicVector;
    dynamicVector.AddToDynamicVector(1);
    assert(dynamicVector.GetSizeOfDynamicVector() == 1);
    assert(dynamicVector[0] == 1);

    dynamicVector.AddToDynamicVector(2);
    dynamicVector.AddToDynamicVector(3);
    dynamicVector.AddToDynamicVector(4);
    dynamicVector.AddToDynamicVector(5);
    dynamicVector.AddToDynamicVector(6);
    dynamicVector.AddToDynamicVector(7);
    dynamicVector.AddToDynamicVector(8);
    dynamicVector.AddToDynamicVector(9);
    dynamicVector.AddToDynamicVector(10);
    dynamicVector.AddToDynamicVector(11);
    dynamicVector.AddToDynamicVector(12);
    dynamicVector.AddToDynamicVector(13);
    dynamicVector.AddToDynamicVector(14);
    dynamicVector.AddToDynamicVector(15);
    assert(dynamicVector.GetSizeOfDynamicVector() == 15);
    assert(dynamicVector[0] == 1);
    assert(dynamicVector[1] == 2);
    assert(dynamicVector[2] == 3);
    assert(dynamicVector[3] == 4);
    assert(dynamicVector[4] == 5);
    assert(dynamicVector[5] == 6);
    assert(dynamicVector[6] == 7);
    assert(dynamicVector[7] == 8);
    assert(dynamicVector[8] == 9);
    assert(dynamicVector[9] == 10);
    assert(dynamicVector[10] == 11);
}

void TestDynamicVector::testDynamicVectorRemove() {
    DynamicVector<int> dynamicVector;
    dynamicVector.AddToDynamicVector(1);
    dynamicVector.AddToDynamicVector(2);
    dynamicVector.AddToDynamicVector(3);

    dynamicVector.RemoveFromDynamicVector(1);
    assert(dynamicVector.GetSizeOfDynamicVector() == 2);
    assert(dynamicVector[0] == 1);
    assert(dynamicVector[1] == 3);

    dynamicVector.RemoveFromDynamicVector(1);
    assert(dynamicVector.GetSizeOfDynamicVector() == 1);
    assert(dynamicVector[0] == 1);
}

void TestDynamicVector::testDynamicVectorOperator() {
    DynamicVector<int> dynamicVector;
    dynamicVector.AddToDynamicVector(1);
    dynamicVector.AddToDynamicVector(2);
    dynamicVector.AddToDynamicVector(3);

    assert(dynamicVector[0] == 1);
    assert(dynamicVector[1] == 2);
    assert(dynamicVector[2] == 3);
}

void TestDynamicVector::testDynamicVectorSize() {
    DynamicVector<int> dynamicVector;
    assert(dynamicVector.GetSizeOfDynamicVector() == 0);

    dynamicVector.AddToDynamicVector(1);
    assert(dynamicVector.GetSizeOfDynamicVector() == 1);

    dynamicVector.AddToDynamicVector(2);
    dynamicVector.AddToDynamicVector(3);
    dynamicVector.AddToDynamicVector(4);
    dynamicVector.AddToDynamicVector(5);
    dynamicVector.AddToDynamicVector(6);
    dynamicVector.AddToDynamicVector(7);
    dynamicVector.AddToDynamicVector(8);
    dynamicVector.AddToDynamicVector(9);
    dynamicVector.AddToDynamicVector(10);
    dynamicVector.AddToDynamicVector(11);
    dynamicVector.AddToDynamicVector(12);
    dynamicVector.AddToDynamicVector(13);
    dynamicVector.AddToDynamicVector(14);
    dynamicVector.AddToDynamicVector(15);
    assert(dynamicVector.GetSizeOfDynamicVector() == 15);
}

void TestDynamicVector::testDynamicVectorSearch() {
    DynamicVector<int> dynamicVector;
    dynamicVector.AddToDynamicVector(1);
    dynamicVector.AddToDynamicVector(2);
    dynamicVector.AddToDynamicVector(3);
    dynamicVector.AddToDynamicVector(4);
    dynamicVector.AddToDynamicVector(5);
    dynamicVector.AddToDynamicVector(6);
    dynamicVector.AddToDynamicVector(7);

    assert(dynamicVector.SearchInDynamicVector(1) == true);
    assert(dynamicVector.SearchInDynamicVector(2) == true);
    assert(dynamicVector.SearchInDynamicVector(3) == true);
    assert(dynamicVector.SearchInDynamicVector(4) == true);
    assert(dynamicVector.SearchInDynamicVector(5) == true);
    assert(dynamicVector.SearchInDynamicVector(6) == true);
    assert(dynamicVector.SearchInDynamicVector(7) == true);
    assert(dynamicVector.SearchInDynamicVector(8) == false);
    assert(dynamicVector.SearchInDynamicVector(9) == false);
    assert(dynamicVector.SearchInDynamicVector(10) == false);
}
