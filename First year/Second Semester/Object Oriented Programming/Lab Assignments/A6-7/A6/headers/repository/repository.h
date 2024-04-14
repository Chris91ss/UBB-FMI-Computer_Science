#pragma once
#include <vector>
#include <algorithm>
#include <stdexcept>
#include "trenchCoat.h"
using namespace std;

class Repository {
protected:

    double totalBasketPrice = 0;
    vector<TrenchCoat> elements;

public:
    Repository();
    Repository(const Repository &other);
    ~Repository();
    TrenchCoat &operator[](int index);

    virtual void Add(const TrenchCoat& elem);
    virtual void Remove(int index);
    virtual void RemoveByValue(const TrenchCoat& elem);
    unsigned long long GetSize();
    vector<TrenchCoat> GetAll();
    bool Search(const TrenchCoat& elem) const;

    double GetTotalBasketPrice() const;
    void SetTotalBasketPrice(double newTotalBasketPrice);
};
