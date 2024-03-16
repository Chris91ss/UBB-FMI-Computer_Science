#pragma once
#include "../service/service.h"

typedef struct {
    Service *service;
} UI;

UI *CreateUI(Service *service);
void DestroyUI(UI *ui);

void RunApp(UI *ui);
void GenerateRandomData(UI *ui);
void PrintMenu();
void PrintTitle();
void AddEstateUI(UI *ui);
void DeleteEstateUI(UI *ui);
void UpdateEstateUI(UI *ui);
void DisplayEstatesUI(UI *ui);
void DisplayEstatesContainingStringUI(UI *ui);
void DisplayEstatesOfGivenTypeUI(UI *ui);