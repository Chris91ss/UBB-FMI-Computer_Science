#pragma once
#include <iostream>
#include <fstream>
#include <stdexcept>
#include "repository.h"
using namespace std;

class TextRepository : public Repository{
private:
    string fileName;
public:
    explicit TextRepository(const string& fileName);
    TextRepository();

    void Add(const TrenchCoat& trenchCoat) override;
    void Remove(int index) override;
    void RemoveByValue(const TrenchCoat& trenchCoat) override;
    void writeToFile();
    void readFromFile();
};