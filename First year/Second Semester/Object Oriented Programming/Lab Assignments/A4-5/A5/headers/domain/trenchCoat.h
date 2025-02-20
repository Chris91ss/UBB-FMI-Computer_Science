#pragma once
#include <string>

using namespace std;

class TrenchCoat
{
private:
    string size;
    string color;
    double price;
    int quantity;
    string photograph;

public:
    TrenchCoat(); // default constructor with default values
    TrenchCoat(const string& size, const string& color, double price, int quantity, const string& photograph); // constructor with parameters
    TrenchCoat(const TrenchCoat &trenchCoat); // copy constructor
    ~TrenchCoat(); // destructor
    TrenchCoat &operator=(const TrenchCoat &trenchCoat); // assignment operator
    bool operator==(const TrenchCoat &trenchCoat) const;

    string GetSize() const;
    string GetColor() const;
    double GetPrice() const;
    int GetQuantity() const;
    string GetPhotograph() const;

    void SetPrice(double newPrice);
    void SetQuantity(int newQuantity);
    void SetPhotograph(const string &newPhotograph);

};