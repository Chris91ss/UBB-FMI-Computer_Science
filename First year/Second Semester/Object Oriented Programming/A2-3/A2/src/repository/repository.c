#pragma once
#include <string.h>
#include "../../headers/domain/estate.h"

Estate estates[100];

int add(Estate estate) {
    for (int i = 0; i < 100; i++) {
        if (strcmp(estates[i].address, "") == 0) {
            estates[i] = estate;
            return 1;
        }
    }
    return 0;
}

int delete(const char* address)
{
    for (int i = 0; i < 100; i++) {
        if (strcmp(estates[i].address, address) == 0) {
            strcpy(estates[i].address, "");
            estates[i].type = -1;
            estates[i].surface = -1;
            estates[i].price = -1;
            return 1;
        }
    }
    return 0;
}

int update(const char* address, EstateType new_type, float new_surface, float new_price)
{
    for (int i = 0; i < 100; i++) {
        if (strcmp(estates[i].address, address) == 0) {
            estates[i].type = new_type;
            estates[i].surface = new_surface;
            estates[i].price = new_price;
            return 1;
        }
    }
    return 0;
}

Estate* GetAll()
{
    return estates;
}
