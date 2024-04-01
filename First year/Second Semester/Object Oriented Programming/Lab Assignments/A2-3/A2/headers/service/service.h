#include "../domain/estate.h"
#pragma once

int AddEstate(Estate estate);
int DeleteEstate(const char* address);
int UpdateEstate(const char* address, EstateType new_type, float new_surface, float new_price);
Estate* GetAllEstates();