#pragma once


typedef void *TElem;

typedef void (*DestroyFunction)(void*);

typedef struct {
    TElem *elems;
    int length;
    int capacity;
    DestroyFunction destroyFunction;
}DynamicArray;

DynamicArray* CreateDynamicArray(int capacity, DestroyFunction destroyFunction);

void DestroyDynamicArray(DynamicArray *dynamicArray);

void ResizeDynamicArray(DynamicArray *dynamicArray);

int AddElementToDynamicArray(DynamicArray *dynamicArray, TElem element);

int RemoveElementFromDynamicArray(DynamicArray *dynamicArray, int position);

TElem GetDynamicArray(DynamicArray *dynamicArray, int position);