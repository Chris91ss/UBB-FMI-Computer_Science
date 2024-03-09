#include <stdio.h>
#include <string.h>
#include "../../headers/domain/estate.h"


Estate CreateEstate(EstateType type, const char* address, float surface, float price) {
    Estate new_estate;
    new_estate.type = type;
    // we can use snprintf(new_estate.address, sizeof(new_estate.address), "%s", address); or
    strcpy(new_estate.address, address);
    new_estate.surface = surface;
    new_estate.price = price;
    return new_estate;
}

void DisplayEstate(Estate estate) {
    const char* type_str;
    switch (estate.type) {
        case HOUSE:
            type_str = "House";
            break;
        case APARTMENT:
            type_str = "Apartment";
            break;
        case PENTHOUSE:
            type_str = "Penthouse";
            break;
        default:
            type_str = "Unknown";
            break;
    }
    printf("Type: %s \n Address: %s \n Surface: %.2f square meters \n Price: $%.2f \n",
           type_str, estate.address, estate.surface, estate.price);
}

