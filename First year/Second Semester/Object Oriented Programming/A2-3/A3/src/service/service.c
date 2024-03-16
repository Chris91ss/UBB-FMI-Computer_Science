#include "../../headers/domain/estate.h"
#include "../../headers/repository/repository.h"
#include "../../headers/service/service.h"
#include <stdlib.h>
#include <string.h>

#pragma once

Service* CreateService(Repository *repository)
{
    Service *service = (Service *) malloc(sizeof(Service));
    service->repository = repository;
    return service;
}

void DestroyService(Service *service)
{
    DestroyRepository(service->repository);
    free(service);
}

int AddEstate(Service *service, Estate *estate) {
    if(GetEstate(service->repository, GetEstateAddress(estate)) != NULL)
        return 0;

    return Add(service->repository, estate);
}

int DeleteEstate(Service *service, const char* address) {
    return Delete(service->repository, address);
}

int UpdateEstate(Service *service, const char* address, EstateType new_type, double new_surface, double new_price) {
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



