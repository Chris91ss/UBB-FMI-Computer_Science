#include "../../headers/domain/trenchCoat.h"

TrenchCoat::TrenchCoat() {
    this->size = "";
    this->color = "";
    this->price = 0;
    this->quantity = 0;
    this->photograph = "";

}

TrenchCoat::TrenchCoat(const string &size, const string &color, double price, int quantity, const string &photograph)
{
    this->size = size;
    this->color = color;
    this->price = price;
    this->quantity = quantity;
    this->photograph = photograph;
}

TrenchCoat::TrenchCoat(const TrenchCoat &trenchCoat) {
    this->size = trenchCoat.size;
    this->color = trenchCoat.color;
    this->price = trenchCoat.price;
    this->quantity = trenchCoat.quantity;
    this->photograph = trenchCoat.photograph;
}

TrenchCoat::~TrenchCoat() = default;

TrenchCoat &TrenchCoat::operator=(const TrenchCoat &trenchCoat) {
    if (this == &trenchCoat)
        return *this;

    this->size = trenchCoat.size;
    this->color = trenchCoat.color;
    this->price = trenchCoat.price;
    this->quantity = trenchCoat.quantity;
    this->photograph = trenchCoat.photograph;
    return *this;
}


bool TrenchCoat::operator==(const TrenchCoat &trenchCoat) const {
    return this->size == trenchCoat.size && this->color == trenchCoat.color;
}

istream &operator>>(istream &input, TrenchCoat &trenchCoat) {
    string line;
    getline(input, line);

    vector<string> tokens = tokenize(line, ',');

    if (tokens.size() != 5) {
        return input;
    }

    trenchCoat.size = tokens[0];
    trenchCoat.color = tokens[1];
    trenchCoat.price = stod(tokens[2]);
    trenchCoat.quantity = stoi(tokens[3]);
    trenchCoat.photograph = tokens[4];

    return input;
}

ostream &operator<<(ostream &output, const TrenchCoat &trenchCoat) {
    output << trenchCoat.size << "," << trenchCoat.color << "," << trenchCoat.price << "," << trenchCoat.quantity << "," << trenchCoat.photograph << "\n";
    return output;
}

string TrenchCoat::GetSize() const {
    return this->size;
}

string TrenchCoat::GetColor() const {
    return this->color;
}

double TrenchCoat::GetPrice() const {
    return this->price;
}

int TrenchCoat::GetQuantity() const {
    return this->quantity;
}

string TrenchCoat::GetPhotograph() const {
    return this->photograph;
}

void TrenchCoat::SetPrice(double newPrice) {
    this->price = newPrice;
}

void TrenchCoat::SetQuantity(int newQuantity) {
    this->quantity = newQuantity;
}

void TrenchCoat::SetPhotograph(const string &newPhotograph) {
    this->photograph = newPhotograph;
}

string TrenchCoat::toString() const {
    return this->size + " " + this->color + " " + std::to_string(this->price) + " " + std::to_string(this->quantity) + " " + this->photograph;
}

