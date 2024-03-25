#pragma once
#include "../../headers/domain/trenchCoat.h"
#include "../../headers/repository/repository.h"
#include <cassert>

class TestRepository
{
public:
    static void testAllRepository();
private:
    static void testRepositoryConstructors();
    static void testRepositoryAdd();
    static void testRepositoryRemove();
    static void testRepositorySize();
    static void testRepositoryGetAll();
    static void testRepositorySearch();
};