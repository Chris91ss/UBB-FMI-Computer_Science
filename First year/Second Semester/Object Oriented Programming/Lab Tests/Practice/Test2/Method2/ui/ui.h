#pragma once
#include "../repository/person.h"
#include <iostream>
#include <limits>

class UI {
public:
    explicit UI(Person& person);
    void run();
    ~UI() = default;
private:
    Person& person;
    static void clearInput();
    static void printMenu();
    void addAnalysis();
    void printAnalyses();
    void printAnalysesByMonth();
    void printIllness();
    void printAnalysesBetweenDates();
    void writeToFile();
};