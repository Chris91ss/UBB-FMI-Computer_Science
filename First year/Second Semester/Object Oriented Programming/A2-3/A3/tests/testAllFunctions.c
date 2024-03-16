#include "testDomain/testDynamicArray.h"
#include "testDomain/testEstate.h"
#include "testDomain/testStack.h"
#include "testRepo/testRepository.h"
#include "testService/testService.h"

void TestAllFunctions()
{
    TestDynamicArray();
    TestEstate();
    TestStack();
    TestRepository();
    TestService();
}