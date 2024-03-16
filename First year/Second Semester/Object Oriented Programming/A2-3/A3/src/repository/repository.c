#pragma once
#include <string.h>
#include <stdlib.h>
#include "../../headers/domain/estate.h"
#include "../../headers/repository/repository.h"

Repository *CreateRepository() {
    Repository *repository = (Repository *) malloc(sizeof(Repository));
    repository->estates = CreateDynamicArray(2, (DestroyFunction) DestroyEstate);
    return repository;
}

void DestroyRepository(Repository *repository) {
    DestroyDynamicArray(repository->estates);
    free(repository);
}

int Add(Repository *repository, Estate *estate) {
    return AddElementToDynamicArray(repository->estates, estate);
}

int Delete(Repository *repository, const char *address) {
    for (int i = 0; i < repository->estates->length; i++) {
        Estate *estate = (Estate *) repository->estates->elems[i];
        if (strcmp(GetEstateAddress(estate), address) == 0)
            return RemoveElementFromDynamicArray(repository->estates, i);
    }
    return 0;
}

int Update(Repository *repository, const char *address, EstateType new_type, double new_surface, double new_price) {
    for (int i = 0; i < repository->estates->length; i++) {
        Estate *estate = (Estate *) repository->estates->elems[i];
        if (strcmp(GetEstateAddress(estate), address) == 0) {
            SetEstateType(estate, new_type);
            SetEstateSurface(estate, new_surface);
            SetEstatePrice(estate, new_price);
            return 1;
        }
    }
    return 0;
}

Estate *GetEstate(Repository *repository, const char *address) {
    for (int i = 0; i < repository->estates->length; i++) {
        Estate *estate = (Estate *) repository->estates->elems[i];
        if (strcmp(GetEstateAddress(estate), address) == 0)
            return estate;
    }
    return NULL;
}

DynamicArray *GetAll(Repository *repository) {
    return repository->estates;
}
