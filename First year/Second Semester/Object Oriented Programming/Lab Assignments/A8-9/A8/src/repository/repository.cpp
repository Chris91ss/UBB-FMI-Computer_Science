#include "../../headers/repository/repository.h"


Repository::Repository() = default;

Repository::Repository(const Repository &other) {
    this->elements = other.elements;
}

Repository::~Repository() = default;

TrenchCoat &Repository::operator[](int index) {
    return this->elements[index];
}

void Repository::Add(const TrenchCoat& elem) {
    this->elements.push_back(elem);
}

void Repository::Remove(int index) {
    this->elements.erase(this->elements.begin() + index);
}

void Repository::RemoveByValue(const TrenchCoat &elem) {
    auto it = find(this->elements.begin(), this->elements.end(), elem);
    if (it != this->elements.end())
        this->elements.erase(it);
}

unsigned long long Repository::GetSize() {
    return this->elements.size();
}

vector<TrenchCoat> Repository::GetAll() {
    return this->elements;
}

bool Repository::Search(const TrenchCoat& elem) const {
    auto it = find(this->elements.begin(), this->elements.end(), elem);
    return it != this->elements.end();
}

double Repository::GetTotalBasketPrice() const {
    return this->totalBasketPrice;
}

void Repository::SetTotalBasketPrice(double newTotalBasketPrice) {
    this->totalBasketPrice = newTotalBasketPrice;
}

void Repository::WriteToFile() {
    throw RepositoryException("Not implemented!");
}

void Repository::ReadFromFile() {
    throw RepositoryException("Not implemented!");
}

void Repository::OpenInApplication() {
    throw RepositoryException("Not implemented!");
}


