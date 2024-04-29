#include "dataBaseRepository.h"

DataBaseRepository::DataBaseRepository(const string& fileName) : fileName(fileName), db(nullptr){
    int rc = sqlite3_open(fileName.c_str(), &db);
    if (rc != SQLITE_OK) {
        throw std::runtime_error("Error opening SQLite database");
    }
    const char* createTableSQL = "CREATE TABLE IF NOT EXISTS trenchcoats (id INTEGER PRIMARY KEY, size TEXT, color TEXT, price REAL, quantity INTEGER, photograph TEXT)";
    char* errMsg;
    rc = sqlite3_exec(db, createTableSQL, nullptr, nullptr, &errMsg);
    if (rc != SQLITE_OK) {
        sqlite3_free(errMsg);
        sqlite3_close(db);
        throw std::runtime_error("Error creating table");
    }
}

DataBaseRepository::~DataBaseRepository() {
    if (db) {
        sqlite3_close(db);
    }
}

void DataBaseRepository::Add(const TrenchCoat& trenchCoat) {
    Repository::Add(trenchCoat);

    string sql = "INSERT INTO trenchcoats (size, color, price, quantity, photograph) VALUES (?, ?, ?, ?, ?)";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        throw std::runtime_error("Error preparing statement for insertion");
    }
    sqlite3_bind_text(stmt, 1, trenchCoat.GetSize().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, trenchCoat.GetColor().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_double(stmt, 3, trenchCoat.GetPrice());
    sqlite3_bind_int(stmt, 4, trenchCoat.GetQuantity());
    sqlite3_bind_text(stmt, 5, trenchCoat.GetPhotograph().c_str(), -1, SQLITE_STATIC);
    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        throw std::runtime_error("Error inserting trench coat");
    }
    sqlite3_finalize(stmt);
}

void DataBaseRepository::Remove(int id) {
    Repository::Remove(id);

    string sql = "DELETE FROM trenchcoats WHERE id = ?";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        throw std::runtime_error("Error preparing statement for deletion");
    }
    sqlite3_bind_int(stmt, 1, id);
    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        throw std::runtime_error("Error deleting trench coat");
    }
    sqlite3_finalize(stmt);
}

void DataBaseRepository::RemoveByValue(const TrenchCoat& trenchCoat) {
    Repository::RemoveByValue(trenchCoat);

    string sql = "DELETE FROM trenchcoats WHERE size = ? AND color = ? AND price = ? AND quantity = ? AND photograph = ?";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        throw std::runtime_error("Error preparing statement for deletion by value");
    }
    sqlite3_bind_text(stmt, 1, trenchCoat.GetSize().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, trenchCoat.GetColor().c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_double(stmt, 3, trenchCoat.GetPrice());
    sqlite3_bind_int(stmt, 4, trenchCoat.GetQuantity());
    sqlite3_bind_text(stmt, 5, trenchCoat.GetPhotograph().c_str(), -1, SQLITE_STATIC);
    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        throw std::runtime_error("Error deleting trench coat by value");
    }
    sqlite3_finalize(stmt);
}

void DataBaseRepository::readFromFile() {
    const char* sql = "SELECT * FROM trenchcoats";
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        throw std::runtime_error("Error preparing statement for reading");
    }
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        string size = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        string color = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        double price = sqlite3_column_double(stmt, 3);
        int quantity = sqlite3_column_int(stmt, 4);
        string photograph = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
        TrenchCoat trenchCoat(size, color, price, quantity, photograph);
        elements.push_back(trenchCoat);
    }
    if (rc != SQLITE_DONE) {
        throw std::runtime_error("Error reading trench coats");
    }
    sqlite3_finalize(stmt);
}
