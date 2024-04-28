#pragma once
#include "repository.h"
#include <fstream>

class HTMLRepository : public Repository {
private:
    string fileName;
public:
    explicit HTMLRepository(string fileName);
    void WriteToFile() override;
    void OpenInApplication() override;
};