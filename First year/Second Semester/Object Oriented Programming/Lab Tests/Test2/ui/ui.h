#pragma once
#include "../repository/repository.h"
#include "../domain/refrigerator.h"
#include "../domain/dishWasher.h"
#include <iostream>

class UI {
public:
    Repository &repo;
    explicit UI(Repository &repo);
    void run();
    ~UI() = default;
private:
    static void printMenu();
    void addAppliance();
    void printAllAppliances() const;
    void printInefficientAppliances() const;
    void writeToFile() const;
};