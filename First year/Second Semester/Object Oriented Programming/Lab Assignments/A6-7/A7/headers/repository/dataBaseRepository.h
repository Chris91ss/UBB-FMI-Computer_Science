#pragma once
#include "repository.h"
#include "repository/dataBaseLibrary/sqlite3.h"

class DataBaseRepository : public Repository {
private:
    string fileName;
    sqlite3* db{};
public:
    explicit DataBaseRepository(const string& fileName);
    DataBaseRepository() = default;
    ~DataBaseRepository(); // Define a destructor to close the database connection

    void Add(const TrenchCoat& trenchCoat) override;
    void Remove(int index) override;
    void RemoveByValue(const TrenchCoat& trenchCoat) override;
    void readFromFile();
};
