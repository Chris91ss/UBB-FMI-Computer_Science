#pragma once
#include "service/service.h"
#include <iostream>

class UI {
private:
    Service service;
public:
    UI(Service &service);
    ~UI();

    void Run();

private:
    static void PrintMenu();
    void AddTaskUI();
    void DisplayTasksUI();
    void DisplayFilteredAndSortedTasksUI();
};