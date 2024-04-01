#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "../../headers/domain/estate.h"


Estate *CreateEstate(EstateType type, const char* address, double surface, double price) {
    Estate *new_estate = (Estate *) malloc(sizeof(Estate));
    new_estate->address = (char *) malloc(strlen(address) + 1);

    new_estate->type = type;
    strcpy(new_estate->address, address);
    new_estate->surface = surface;
    new_estate->price = price;
    return new_estate;
}

void DestroyEstate(Estate *estate) {
    free(estate->address);
    free(estate);
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
    printf("------------------------------------------- \n "
           "Type: %s \n"
           " Address: %s \n"
           " Surface: %.2f square meters \n"
           " Price: $%.2f \n",
           type_str, estate.address, estate.surface, estate.price);
}

Estate *CopyEstate(Estate *estate) {
    Estate *copy = (Estate *) malloc(sizeof(Estate));
    copy->address = (char *) malloc(strlen(estate->address) + 1);

    copy->type = estate->type;
    strcpy(copy->address, estate->address);
    copy->surface = estate->surface;
    copy->price = estate->price;

    return copy;
}

EstateType GetEstateType(Estate *estate) {
    return estate->type;
}

char *GetEstateAddress(Estate *estate) {
    return estate->address;
}

double GetEstateSurface(Estate *estate) {
    return estate->surface;
}

double GetEstatePrice(Estate *estate) {
    return estate->price;
}

void SetEstateType(Estate *estate, EstateType type) {
    estate->type = type;
}

void SetEstateSurface(Estate *estate, double surface) {
    estate->surface = surface;
}

void SetEstatePrice(Estate *estate, double price) {
    estate->price = price;
}

int CompareEstateSurfaceAscending(Estate *estate1, Estate *estate2) {
    return estate1->surface > estate2->surface;
}

int CompareEstateSurfaceDescending(Estate *estate1, Estate *estate2) {
    return estate1->surface < estate2->surface;
}
