#pragma once
#include "../../headers/domain/dynamicVector.h"
#include <cassert>

class TestDynamicVector {
public:
    static void testAllDynamicVector();
private:
    static void testDynamicVectorConstructors();
    static void testDynamicVectorAdd();
    static void testDynamicVectorRemove();
    static void testDynamicVectorOperator();
    static void testDynamicVectorSize();
    static void testDynamicVectorSearch();
};