#include "../../headers/domain/estate.h"
#include "../../headers/repository/repository.h"
#pragma once

int AddEstate(Estate estate) {
    return add(estate);
}

int DeleteEstate(const char* address) {
    return delete(address);
}

int UpdateEstate(const char* address, EstateType new_type, float new_surface, float new_price) {
    return update(address, new_type, new_surface, new_price);
}

Estate* GetAllEstates() {
    Estate* estates = GetAll();
    for (int i = 0; i < 100; i++) {
        for (int j = i + 1; j < 100; j++) {
            if (estates[i].price > estates[j].price) {
                Estate aux = estates[i];
                estates[i] = estates[j];
                estates[j] = aux;
            }
        }
    }
    return estates;
}