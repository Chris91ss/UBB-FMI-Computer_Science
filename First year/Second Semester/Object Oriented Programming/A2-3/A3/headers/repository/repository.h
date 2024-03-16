#include "../domain/estate.h"
#include "../domain/dynamicArray.h"

#pragma once

typedef struct {
    DynamicArray *estates;
} Repository;

Repository *CreateRepository();
void DestroyRepository(Repository *repository);
Repository *CopyRepository(Repository *repository);

int Add(Repository *repository, Estate *estate);
int Delete(Repository *repository, const char* address);
int Update(Repository *repository,const char* address, EstateType new_type, double new_surface, double new_price);
Estate *GetEstate(Repository *repository, const char* address);
DynamicArray* GetAll(Repository *repository);
