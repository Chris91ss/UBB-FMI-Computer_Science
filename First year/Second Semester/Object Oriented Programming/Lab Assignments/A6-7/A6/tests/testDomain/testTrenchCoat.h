#pragma once
#include "../../headers/domain/trenchCoat.h"
#include <cassert>

class TestTrenchCoat {
public:
    static void testAllTrenchCoat();

private:
    static void testTrenchCoatConstructors();
    static void testTrenchCoatOperator();
    static void testTrenchCoatGetters();
    static void testTrenchCoatSetters();
};