#include "test.h"

void Test::TestAll() {
    TestDynamicVector::testAllDynamicVector();
    TestTrenchCoat::testAllTrenchCoat();
    TestRepository::testAllRepository();
    TestService::testAllService();
}
