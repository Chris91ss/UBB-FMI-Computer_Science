#pragma once
#include "../service/service.h"
#include <iostream>

class UI {
private:
    Service service;

public:
    UI(const Service &service);
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
};