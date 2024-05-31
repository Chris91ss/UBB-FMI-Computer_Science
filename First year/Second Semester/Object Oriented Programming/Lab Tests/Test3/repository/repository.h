#pragma once
#include <vector>
#include "../domain/disorder.h"
using namespace std;

class Repository {
private:
    vector<Disorder*> disorders;
public:
    Repository() = default;
    ~Repository() = default;
    void addDisorder(Disorder* disorder);
    vector<Disorder*> getDisorders() const;
    vector<Disorder*> getDisordersSorted() const;
};
