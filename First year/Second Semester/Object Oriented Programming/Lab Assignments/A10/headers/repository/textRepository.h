#pragma once
#include <iostream>
#include <fstream>
#include <stdexcept>
#include "repository.h"
#include "../utilities/exceptions.h"
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
    void WriteToFile() override;
    void readFromFile();
};