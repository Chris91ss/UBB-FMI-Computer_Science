#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../headers/ui/ui.h"
#pragma once

UI *CreateUI(Service *service)
{
    UI *ui = (UI *) malloc(sizeof(UI));
    ui->service = service;
    return ui;
}

void DestroyUI(UI *ui)
{
    DestroyService(ui->service);
    free(ui);
}

void RunApp(UI *ui)
{
    int option;
    GenerateRandomData(ui);
    PrintTitle();

    while (1)
    {
        PrintMenu();
        printf("Option: ");
        scanf("%d", &option);
        switch (option)
        {
        case 1:
            AddEstateUI(ui);
            break;
        case 2:
            DeleteEstateUI(ui);
            break;
        case 3:
            UpdateEstateUI(ui);
            break;
        case 4:
            DisplayEstatesUI(ui);
            break;
        case 5:
            DisplayEstatesContainingStringUI(ui);
            break;
        case 6:
            DisplayEstatesOfGivenTypeUI(ui);
            break;
        case 7:
            UndoUI(ui);
            break;
        case 8:
            RedoUI(ui);
            break;
        case 9:
            printf("Exiting...\n");
            exit(0);
        default:
            printf("Invalid option!\n");
            break;
        }
    }
}

void PrintMenu()
{
    printf("1. Add Estate.\n");
    printf("2. Delete Estate.\n");
    printf("3. Update Estate.\n");
    printf("4. Display Estates.\n");
    printf("5. Display Estates sorted by their price or surface, by a given string.\n");
    printf("6. Display Estates of a given type, having the surface greater than a provided value, in descending or ascending order.\n");
    printf("7. Undo last operation.\n");
    printf("8. Redo last operation.\n");
    printf("9. Exit...\n");
}

void PrintTitle()
{
    printf("----------------------------------------------------------------------\n");
    printf("--------------------------REAL ESTATE AGENCY--------------------------\n");
    printf("----------------------------------------------------------------------\n");
}

void GenerateRandomData(UI *ui)
{
    Estate *estate1 = CreateEstate(HOUSE, "Street Venus", 124, 300000);
    Estate *estate2 = CreateEstate(APARTMENT, "Main Street", 77, 255000);
    Estate *estate3 = CreateEstate(PENTHOUSE, "Street Teodor", 220, 500000);
    Estate *estate4 = CreateEstate(HOUSE, "Street Alexandru Vaida", 169, 400000);
    Estate *estate5 = CreateEstate(APARTMENT, "1st Street", 55, 600000);
    Estate *estate6 = CreateEstate(PENTHOUSE, "2nd Street", 120, 195000);
    Estate *estate7 = CreateEstate(HOUSE, "3rd Street", 178, 289000);
    Estate *estate8 = CreateEstate(APARTMENT, "4th Street", 85, 124999);
    Estate *estate9 = CreateEstate(PENTHOUSE, "5th Street", 190, 555000);
    Estate *estate10 = CreateEstate(HOUSE, "6th Street", 240, 333399);
    Estate *estate11 = CreateEstate(APARTMENT, "7th Street", 105, 450990);
    Estate *estate12 = CreateEstate(PENTHOUSE, "8th Street", 400, 799999);
    AddEstate(ui->service, estate1);
    AddEstate(ui->service, estate2);
    AddEstate(ui->service, estate3);
    AddEstate(ui->service, estate4);
    AddEstate(ui->service, estate5);
    AddEstate(ui->service, estate6);
    AddEstate(ui->service, estate7);
    AddEstate(ui->service, estate8);
    AddEstate(ui->service, estate9);
    AddEstate(ui->service, estate10);
    AddEstate(ui->service, estate11);
    AddEstate(ui->service, estate12);
}

void AddEstateUI(UI *ui)
{
    EstateType type;
    char address[31];
    float surface, price;
    printf("Type (0 - House, 1 - Apartment, 2 - Penthouse): \n");
    while(1){
        scanf("%d", &type);
        if(type == 0 || type == 1 || type == 2) {
            break;
        }
        printf("Invalid type! Type (0 - House, 1 - Apartment, 2 - Penthouse): \n");
    }
    printf("Type an Address: \n");
    scanf(" %[^\n]", address);
    printf("Type a Surface: \n");
    scanf("%f", &surface);
    printf("Type a Price: \n");
    scanf("%f", &price);
    Estate *new_estate = CreateEstate(type, address, surface, price);
    int result = AddEstate(ui->service, new_estate);
    if (result)
    {
        printf("Estate added successfully!\n");
    }
    else
    {
        printf("Estate could not be added!\n");
    }
}

void DeleteEstateUI(UI *ui)
{
    char address[31];
    printf("Type an Address: ");
    scanf(" %[^\n]", address);
    printf("Address: %s\n", address);
    int result = DeleteEstate(ui->service, address);
    if (result)
    {
        printf("Estate deleted successfully!\n");
    }
    else
    {
        printf("Estate could not be deleted!\n");
    }
}

void UpdateEstateUI(UI *ui)
{
    char address[31];
    EstateType new_type;
    float new_surface, new_price;
    printf("Type an Address: \n");
    scanf(" %[^\n]", address);
    printf("Type a new Type (0 - House, 1 - Apartment, 2 - Penthouse): \n");
    while(1)
    {
        scanf("%d", &new_type);
        if(new_type == 0 || new_type == 1 || new_type == 2) {
            break;
        }
        printf("Invalid type! Type a new Type (0 - House, 1 - Apartment, 2 - Penthouse): \n");
    }
    printf("Type a new Surface: \n");
    scanf("%f", &new_surface);
    printf("Type a new Price: \n");
    scanf("%f", &new_price);
    int result = UpdateEstate(ui->service, address, new_type, new_surface, new_price);
    if (result)
    {
        printf("Estate updated successfully!\n");
    }
    else
    {
        printf("Estate could not be updated!\n");
    }
}

void DisplayEstatesUI(UI *ui)
{
    DynamicArray* estates = GetAllEstates(ui->service);

    if(estates->length == 0)
    {
        printf("\n No estates found! \n");
        free(estates->elems);
        free(estates);
        return;
    }

    for(int i = 0; i < estates->length; i++)
    {
        Estate *estate = GetDynamicArray(estates, i);
        DisplayEstate(*estate);
    }
}

void DisplayEstatesContainingStringUI(UI *ui)
{
    char string[31];
    char choice[31];
    GetEstateAttribute GetAttribute = GetEstatePrice;
    printf("Type a string: ");
    scanf(" %[^\n]", string);

    printf("For ascending by price type 'price'\n");
    printf("For ascending by surface type 'surface' \n");
    printf("> ");
    scanf(" %[^\n]", choice);
    while(strcmp(choice, "price") != 0 && strcmp(choice, "surface") != 0)
    {
        printf("Invalid choice! \n");
        printf("For ascending by price type 'price'\n");
        printf("For ascending by surface type 'surface' \n");
        printf("> ");
        scanf(" %[^\n]", choice);
    }

    if(strcmp(choice, "price") == 0){
        GetAttribute = GetEstatePrice;
    }
    else if(strcmp(choice, "surface") == 0){
        GetAttribute = GetEstateSurface;
    }

    DynamicArray *estates = GetAllEstatesContainingString(ui->service, string, GetAttribute);

    if (estates->length == 0)
    {
        printf("\nNo estates found!\n");
        free(estates->elems);
        free(estates);
        return;
    }
    printf("\n The estates with the given string are: \n");
    for (int i = 0; i < estates->length; i++)
    {
        Estate *estate = GetDynamicArray(estates, i);
        DisplayEstate(*estate);
    }
    DestroyDynamicArray(estates);
}

void DisplayEstatesOfGivenTypeUI(UI *ui)
{
    int type;
    char choice[31];
    CompareEstate CompareFunction = CompareEstateSurfaceAscending;

    printf("Type (0 - House, 1 - Apartment, 2 - Penthouse): ");
    while(1)
    {
        scanf("%d", &type);
        if(type == 0 || type == 1 || type == 2) {
            break;
        }
        printf("Invalid type! Type (0 - House, 1 - Apartment, 2 - Penthouse): ");
    }

    float surface;
    printf("Type a surface: ");
    while(1)
    {
        scanf("%f", &surface);
        if(surface > 0) {
            break;
        }
        printf("Invalid surface! Type a surface: ");
    }

    printf("For sorting in ascending order type 'ascending'\n");
    printf("For sorting in descending order type 'descending' \n");
    printf("> ");
    scanf(" %[^\n]", choice);
    while(strcmp(choice, "ascending") != 0 && strcmp(choice, "descending") != 0)
    {
        printf("Invalid choice! \n");
        printf("For sorting in ascending order type 'ascending'\n");
        printf("For sorting in descending order type 'descending' \n");
        printf("> ");
        scanf(" %[^\n]", choice);
    }

    if(strcmp(choice, "ascending") == 0){
        CompareFunction = CompareEstateSurfaceAscending;
    }
    else if(strcmp(choice, "descending") == 0){
        CompareFunction = CompareEstateSurfaceDescending;
    }

    DynamicArray *estates = GetAllEstatesOfTypeHavingSurfaceGreaterThanAValue(ui->service, type, surface, CompareFunction);
    if (estates->length == 0)
    {
        printf("\nNo estates found!\n");
        free(estates->elems);
        free(estates);
        return;
    }

    printf("\n The estates of the given type, sorted in ascending order by price are: \n");
    for (int i = 0; i < estates->length; i++)
    {
        Estate *estate = GetDynamicArray(estates, i);
        DisplayEstate(*estate);
    }
    DestroyDynamicArray(estates);
}

void UndoUI(UI *ui)
{
    int result = Undo(ui->service);
    if (result)
    {
        printf("Undo successful!\n");
    }
    else
    {
        printf("Undo failed!\n");
    }
}

void RedoUI(UI *ui)
{
    int result = Redo(ui->service);
    if (result)
    {
        printf("Redo successful!\n");
    }
    else
    {
        printf("Redo failed!\n");
    }
}

