#include "../../headers/domain/dynamicArray.h"
#pragma once

typedef struct {
    DynamicArray *stack;
    int position;
}Stack;

Stack* CreateStack(int capacity, DestroyFunction destroyFunction);
void DestroyStack(Stack *stack);
int PushStack(Stack *stack, TElem element);
TElem PopStack(Stack *stack);
