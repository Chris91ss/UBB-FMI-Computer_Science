#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../headers/ui/ui.h"
#include "../../headers/domain/estate.h"
#include "../../headers/service/service.h"
#pragma once

void RunApp()
{
    int option;
    GenerateRandomData();
    while (1)
    {
        PrintMenu();
        printf("Option: ");
        scanf("%d", &option);
        switch (option)
        {
        case 1:
            AddEstateUI();
            break;
        case 2:
            DeleteEstateUI();
            break;
        case 3:
            UpdateEstateUI();
            break;
        case 4:
            DisplayEstatesUI();
            break;
        case 5:
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
    printf("4. Display Estates sorted by their price by a given string.\n");
    printf("5. Exit...\n");
}

void GenerateRandomData()
{
    Estate estate1 = CreateEstate(HOUSE, "Street Venus", 124, 300000);
    Estate estate2 = CreateEstate(APARTMENT, "Main Street", 77, 255000);
    Estate estate3 = CreateEstate(PENTHOUSE, "Street Teodor", 220, 500000);
    Estate estate4 = CreateEstate(HOUSE, "Street Alexandru Vaida", 169, 400000);
    Estate estate5 = CreateEstate(APARTMENT, "1st Street", 55, 600000);
    Estate estate6 = CreateEstate(PENTHOUSE, "2nd Street", 120, 195000);
    Estate estate7 = CreateEstate(HOUSE, "3rd Street", 178, 289000);
    Estate estate8 = CreateEstate(APARTMENT, "4th Street", 85, 124999);
    Estate estate9 = CreateEstate(PENTHOUSE, "5th Street", 190, 555000);
    Estate estate10 = CreateEstate(HOUSE, "6th Street", 240, 333399);
    Estate estate11 = CreateEstate(APARTMENT, "7th Street", 105, 450990);
    Estate estate12 = CreateEstate(PENTHOUSE, "8th Street", 400, 799999);
    AddEstate(estate1);
    AddEstate(estate2);
    AddEstate(estate3);
    AddEstate(estate4);
    AddEstate(estate5);
    AddEstate(estate6);
    AddEstate(estate7);
    AddEstate(estate8);
    AddEstate(estate9);
    AddEstate(estate10);
    AddEstate(estate11);
    AddEstate(estate12);
}

void AddEstateUI()
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
    Estate new_estate = CreateEstate(type, address, surface, price);
    int result = AddEstate(new_estate);
    if (result)
    {
        printf("Estate added successfully!\n");
    }
    else
    {
        printf("Estate could not be added!\n");
    }
}

void DeleteEstateUI()
{
    char address[31];
    printf("Type an Address: ");
    scanf(" %[^\n]", address);
    printf("Address: %s\n", address);
    int result = DeleteEstate(address);
    if (result)
    {
        printf("Estate deleted successfully!\n");
    }
    else
    {
        printf("Estate could not be deleted!\n");
    }
}

void UpdateEstateUI()
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
    int result = UpdateEstate(address, new_type, new_surface, new_price);
    if (result)
    {
        printf("Estate updated successfully!\n");
    }
    else
    {
        printf("Estate could not be updated!\n");
    }
}

void DisplayEstatesUI()
{
    Estate* estates = GetAllEstates();
    int foundAddress = 0;
    char findStr[31];
    printf("Type a string to search for in the address: ");
    scanf(" %[^\n]", findStr);
    for (int i = 0; i < 100; i++)
    {
        if(estates[i].address[0] != '\0' && strstr(estates[i].address, findStr) != NULL) {
            DisplayEstate(estates[i]);
            foundAddress = 1;
        }
    }

    if(!foundAddress) {
        for (int i = 0; i < 100; ++i) {
            if(estates[i].address[0] != '\0') {
                DisplayEstate(estates[i]);
            }
        }
    }
}

