#include "../../headers/domain/stack.h"
#include <stdlib.h>

Stack *CreateStack(int capacity, DestroyFunction destroyFunction) {
    Stack *stack = (Stack *) malloc(sizeof(Stack));
    stack->stack = CreateDynamicArray(capacity, destroyFunction);
    stack->position = -1;
    return stack;
}

void DestroyStack(Stack *stack) {
    DestroyDynamicArray(stack->stack);
    free(stack);
}

int PushStack(Stack *stack, TElem element) {
    AddElementToDynamicArray(stack->stack, element);
    stack->position++;
    return 1;
}

TElem PopStack(Stack *stack) {
    if(stack->position == -1)
        return NULL;
    TElem element = stack->stack->elems[stack->position];
    stack->position--;
    return element;
}