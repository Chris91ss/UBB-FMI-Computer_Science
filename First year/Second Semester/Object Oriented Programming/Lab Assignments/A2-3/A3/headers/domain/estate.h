#pragma once

typedef enum {
    HOUSE,
    APARTMENT,
    PENTHOUSE,
} EstateType;

typedef struct {
    EstateType type;
    char *address;
    double surface;
    double price;
} Estate;

typedef double (*GetEstateAttribute)(Estate *);
typedef int (*CompareEstate)(Estate *, Estate *);

Estate *CreateEstate(EstateType type, const char* address, double surface, double price);
void DestroyEstate(Estate *estate);
void DisplayEstate(Estate estate);
Estate *CopyEstate(Estate *estate);

EstateType GetEstateType(Estate *estate);
char *GetEstateAddress(Estate *estate);
double GetEstateSurface(Estate *estate);
double GetEstatePrice(Estate *estate);

void SetEstateType(Estate *estate, EstateType type);
void SetEstateSurface(Estate *estate, double surface);
void SetEstatePrice(Estate *estate, double price);

int CompareEstateSurfaceAscending(Estate *estate1, Estate *estate2);
int CompareEstateSurfaceDescending(Estate *estate1, Estate *estate2);
