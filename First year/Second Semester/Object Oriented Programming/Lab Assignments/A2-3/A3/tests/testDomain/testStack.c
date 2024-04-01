#include <assert.h>
#include "testStack.h"
#include "../../headers/domain/stack.h"
#include "../../headers/domain/estate.h"

void TestStack()
{
    TestCreateStack();
    TestDestroyStack();
    TestPushStack();
    TestPopStack();
}

void TestCreateStack()
{
    Stack* stack = CreateStack(2, (DestroyFunction)DestroyEstate);
    assert(stack->stack->length == 0);
    assert(stack->stack->capacity == 2);
    assert(stack->stack->destroyFunction == (DestroyFunction)DestroyEstate);
    DestroyStack(stack);
}

void TestDestroyStack()
{
    Stack* stack = CreateStack(2, (DestroyFunction)DestroyEstate);
    DestroyStack(stack);
}

void TestPushStack()
{
    Stack* stack = CreateStack(2, (DestroyFunction)DestroyEstate);
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    PushStack(stack, estate);
    assert(stack->stack->length == 1);
    assert(stack->stack->capacity == 2);
    assert(stack->stack->elems[0] == estate);
    DestroyStack(stack);
}

void TestPopStack()
{
    Stack* stack = CreateStack(2, (DestroyFunction)DestroyEstate);
    Estate* estate = CreateEstate(0, "address", 100, 10000);
    PushStack(stack, estate);
    Estate* poppedEstate = PopStack(stack);
    assert(stack->stack->length == 1);
    assert(stack->stack->capacity == 2);
    assert(poppedEstate == estate);
    DestroyStack(stack);
    DestroyEstate(poppedEstate);
}