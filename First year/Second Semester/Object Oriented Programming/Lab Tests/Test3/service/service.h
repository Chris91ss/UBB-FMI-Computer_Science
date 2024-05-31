#pragma once
#include "../repository/repository.h"
#include <fstream>
#include <sstream>

class Service {
private:
    Repository *repository;
public:
    Service(): repository(new Repository()) {}
    explicit Service(Repository *repository);
    ~Service() = default;
    void Add(Disorder *disorder);
    vector<Disorder*> GetDisorders() const;
    vector<Disorder*> GetSortedDisorders() const;
    void readFromFile(const string &filename);
    vector<string> GetDisorderSymptoms(const string &disorderName) const;
    bool searchDisorder(const string &disorderName) const;
};
