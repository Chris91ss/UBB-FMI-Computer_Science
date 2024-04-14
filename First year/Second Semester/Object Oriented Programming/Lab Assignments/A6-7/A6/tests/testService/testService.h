#pragma once
#include "../../headers/domain/trenchCoat.h"
#include "../../headers/service/service.h"
#include <cassert>

class TestService{
public:
    static void testAllService();

private:
    static void testServiceConstructors();
    static void testServiceOperator();
    static void testGenerateEntities();
    static void testServiceAdd();
    static void testServiceRemove();
    static void testServiceUpdate();
    static void testServiceSearch();
    static void testServiceGetAll();
    static void testServiceGetAllFiltered();
    static void testGetSetTotalBasketPrice();
};