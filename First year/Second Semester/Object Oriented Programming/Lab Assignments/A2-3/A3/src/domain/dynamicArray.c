#include "../../headers/domain/dynamicArray.h"
#include <stdlib.h>

DynamicArray* CreateDynamicArray(int capacity, DestroyFunction destroyFunction){
    DynamicArray *dynamicArray = (DynamicArray*)malloc(sizeof(DynamicArray));
    dynamicArray->elems = (TElem*)malloc(capacity * sizeof(TElem));

    dynamicArray->length = 0;
    dynamicArray->capacity = capacity;
    dynamicArray->destroyFunction = destroyFunction;

    return dynamicArray;
}

void DestroyDynamicArray(DynamicArray *dynamicArray){
    for(int i = 0; i < dynamicArray->length; i++){
        dynamicArray->destroyFunction(dynamicArray->elems[i]);
    }
    free(dynamicArray->elems);
    free(dynamicArray);
}

void ResizeDynamicArray(DynamicArray *dynamicArray){
    dynamicArray->elems = (TElem*)realloc(dynamicArray->elems, dynamicArray->capacity * sizeof(TElem));
}

int AddElementToDynamicArray(DynamicArray *dynamicArray, TElem element){
    if(dynamicArray->length == dynamicArray->capacity){
        dynamicArray->capacity *= 2;
        ResizeDynamicArray(dynamicArray);
    }
    dynamicArray->elems[dynamicArray->length++] = element;
    return 1;
}

int RemoveElementFromDynamicArray(DynamicArray *dynamicArray, int position){
    if(position < 0 || position >= dynamicArray->length){
        return 0;
    }
    dynamicArray->destroyFunction(dynamicArray->elems[position]);
    for(int i = position; i < dynamicArray->length - 1; i++){
        dynamicArray->elems[i] = dynamicArray->elems[i + 1];
    }
    dynamicArray->length--;

    if(dynamicArray->length < dynamicArray->capacity / 2 && dynamicArray->capacity > 2){
        dynamicArray->capacity /= 2;
        ResizeDynamicArray(dynamicArray);
    }
    return 1;
}

TElem GetDynamicArray(DynamicArray *dynamicArray, int position){
    if (position < 0 || position >= dynamicArray->length)
        return NULL;
    return dynamicArray->elems[position];
}
