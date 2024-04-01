#include "../domain/estate.h"
#include "../repository/repository.h"
#include "../domain/stack.h"

#pragma once

typedef struct {
    Repository *repository;
    Stack *undoStack;
    Stack *redoStack;
} Service;

Service* CreateService(Repository *repository, Stack *undoStack, Stack *redoStack);
void DestroyService(Service *service);
void SaveBeforeOperation(Service *service);

int AddEstate(Service *service,Estate *estate);
int DeleteEstate(Service *service, const char* address);
int UpdateEstate(Service *service, const char* address, EstateType new_type, double new_surface, double new_price);
DynamicArray* GetAllEstates(Service *service);
DynamicArray* GetAllEstatesContainingString(Service *service, const char* str, GetEstateAttribute GetAttribute);
DynamicArray* GetAllEstatesOfTypeHavingSurfaceGreaterThanAValue(Service *service, EstateType type, double surface, CompareEstate CompareFunction);
void SortEstatesBySurface(DynamicArray *estates, CompareEstate CompareFunction);

int Undo(Service *service);
int Redo(Service *service);