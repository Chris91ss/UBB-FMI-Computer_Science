#pragma once
#include "service/service.h"
#include <iostream>

class UI{
private:
    Service service;
public:
    UI(const Service &service);
    ~UI();
    void run();

private:
    static void printMenu();
    void addBillUI();
    void getAllBillsUI();
    void getAllBillsSortedUI();
    void getAllPaidBillsUI();
    static void exitApp();
};