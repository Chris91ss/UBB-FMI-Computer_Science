#pragma once
#include "repository.h"
#include <fstream>

class HTMLRepository : public Repository {
private:
    string fileName;
public:
    explicit HTMLRepository(string fileName);
    void Add(const TrenchCoat& trenchCoat) override;
    void WriteToFile() override;
    void ReadFromFile() override;
    void OpenInApplication() override;
};