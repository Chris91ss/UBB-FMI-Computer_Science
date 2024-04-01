#pragma once

typedef enum {
    HOUSE,
    APARTMENT,
    PENTHOUSE,
} EstateType;

typedef struct {
    EstateType type;
    char address[31];
    float surface;
    double price;
} Estate;

Estate CreateEstate(EstateType type, const char* address, float surface, float price);
void DisplayEstate(Estate estate);
