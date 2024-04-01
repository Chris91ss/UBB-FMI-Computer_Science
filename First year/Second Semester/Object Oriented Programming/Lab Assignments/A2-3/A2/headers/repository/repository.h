#include "../domain/estate.h"
#pragma once

int add(Estate estate);
int delete(const char* address);
int update(const char* address, EstateType new_type, float new_surface, float new_price);
Estate* GetAll();
