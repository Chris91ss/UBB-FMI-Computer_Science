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
    static void testServiceAdd();
    static void testServiceRemove();
    static void testServiceUpdate();
    static void testServiceGetAll();
};