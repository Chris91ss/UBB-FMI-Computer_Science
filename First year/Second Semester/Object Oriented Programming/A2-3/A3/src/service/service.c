#include "../../headers/domain/estate.h"
#include "../../headers/repository/repository.h"
#include "../../headers/service/service.h"
#include <stdlib.h>
#include <string.h>

#pragma once

Service* CreateService(Repository *repository, Stack *undoStack, Stack *redoStack)
{
    Service *service = (Service *) malloc(sizeof(Service));
    service->repository = repository;
    service->undoStack = undoStack;
    service->redoStack = redoStack;
    return service;
}

void DestroyService(Service *service)
{
    DestroyRepository(service->repository);
    DestroyStack(service->undoStack);
    DestroyStack(service->redoStack);
    free(service);
}

void SaveBeforeOperation(Service *service){
    Repository *repositoryCopy = CopyRepository(service->repository);
    PushStack(service->undoStack, repositoryCopy);
}

int AddEstate(Service *service, Estate *estate) {
    if(GetEstate(service->repository, GetEstateAddress(estate)) != NULL)
        return 0;

    SaveBeforeOperation(service);

    return Add(service->repository, estate);
}

int DeleteEstate(Service *service, const char* address) {
    SaveBeforeOperation(service);

    return Delete(service->repository, address);
}

int UpdateEstate(Service *service, const char* address, EstateType new_type, double new_surface, double new_price) {
    SaveBeforeOperation(service);

    return Update(service->repository, address, new_type, new_surface, new_price);
}

DynamicArray* GetAllEstates(Service *service) {
    return GetAll(service->repository);
}

DynamicArray* GetAllEstatesContainingString(Service *service, const char* str, GetEstateAttribute GetAttribute) {
    DynamicArray *estates = GetAll(service->repository);
    DynamicArray *filteredEstates = CreateDynamicArray(2, (DestroyFunction) DestroyEstate);

    for(int i = 0; i < estates->length; i++) {
        Estate *estate = (Estate *) estates->elems[i];
        if(strstr(GetEstateAddress(estate), str) != NULL)
            AddElementToDynamicArray(filteredEstates, CopyEstate(estate));
    }

    for(int i = 0; i < filteredEstates->length - 1; i++) {
        for(int j = i + 1; j < filteredEstates->length; j++) {
            if(GetAttribute(filteredEstates->elems[i]) > GetAttribute(filteredEstates->elems[j])) {
                void *aux = filteredEstates->elems[i];
                filteredEstates->elems[i] = filteredEstates->elems[j];
                filteredEstates->elems[j] = aux;
            }
        }
    }

    return filteredEstates;
}

DynamicArray* GetAllEstatesOfTypeHavingSurfaceGreaterThanAValue(Service *service, EstateType type, double surface, CompareEstate CompareFunction)
{
    DynamicArray *estates = GetAll(service->repository);
    DynamicArray *filteredEstates = CreateDynamicArray(2, (DestroyFunction) DestroyEstate);

    for(int i = 0; i < estates->length; i++) {
        Estate *estate = (Estate *) estates->elems[i];
        if(GetEstateType(estate) == type && GetEstateSurface(estate) > surface)
            AddElementToDynamicArray(filteredEstates, CopyEstate(estate));
    }

    SortEstatesBySurface(filteredEstates, CompareFunction);
    return filteredEstates;
}

void SortEstatesBySurface(DynamicArray *estates, CompareEstate CompareFunction)
{
    for(int i = 0; i < estates->length - 1; i++) {
        for(int j = i + 1; j < estates->length; j++) {
            if(CompareFunction(estates->elems[i], estates->elems[j])) {
                void *aux = estates->elems[i];
                estates->elems[i] = estates->elems[j];
                estates->elems[j] = aux;
            }
        }
    }
}

int Undo(Service *service) {
    Repository *tempRepository = PopStack(service->undoStack);
    if(tempRepository == NULL)
        return 0;

    PushStack(service->redoStack, CopyRepository(service->repository));
    service->repository = tempRepository;
    return 1;
}

int Redo(Service *service) {
    Repository *tempRepository = PopStack(service->redoStack);
    if(tempRepository == NULL)
        return 0;

    PushStack(service->undoStack, CopyRepository(service->repository));
    service->repository = tempRepository;
    return 1;
}



