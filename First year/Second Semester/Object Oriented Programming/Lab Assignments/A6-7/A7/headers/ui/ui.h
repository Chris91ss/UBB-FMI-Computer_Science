#pragma once
#include "../service/service.h"
#include <iostream>

class UI {
private:
    Service service;
    Service shoppingBasketService;

public:
    UI(const Service &service, const Service &shoppingBasketService);
    ~UI();

    void Run();

private:
    static void PrintTitle();

    static int GetOption();
    static void PrintAdminMenu();
    void RunAdmin();
    static void PrintUserMenu();
    void RunUser();

    void AddTrenchCoat();
    void RemoveTrenchCoat();
    void UpdateTrenchCoat();
    void ListTrenchCoats();
    void ListFilteredTrenchCoats();

    void CycleThroughTrenchCoats();
    void SeeShoppingBasket();
    void SaveShoppingBasket();
    void SeeShoppingBasketOpeningTheSavedFile();
    static void ShoppingBasketMenu();
    int AddToShoppingBasket(const TrenchCoat& trenchCoat);
    void EmptyShoppingBasket();
};