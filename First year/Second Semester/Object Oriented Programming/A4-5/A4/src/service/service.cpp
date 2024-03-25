#include "../../headers/service/service.h"

Service::Service(const Repository<TrenchCoat> &repository) {
    this->repository = repository;
}

Service::Service(const Service &other) {
    this->repository = other.repository;
}

Service::~Service() = default;

Service &Service::operator=(const Service &other) {
    if (this == &other)
        return *this;

    this->repository = other.repository;
    return *this;
}

void Service::Generate10Entities() {
    this->addTrenchCoat("S", "Black", 125, 2, "photo1");
    this->addTrenchCoat("M", "White", 99, 5, "photo2");
    this->addTrenchCoat("L", "Red", 100, 7, "photo3");
    this->addTrenchCoat("XL", "Blue", 450, 1, "photo4");
    this->addTrenchCoat("XXL", "Green", 570, 3, "photo5");
    this->addTrenchCoat("S", "Yellow", 333, 5, "photo6");
    this->addTrenchCoat("M", "Orange", 999, 10, "photo7");
    this->addTrenchCoat("L", "Purple", 128, 15, "photo8");
    this->addTrenchCoat("XL", "Pink", 357, 11, "photo9");
    this->addTrenchCoat("XXL", "Brown", 246, 2, "photo10");
}

void Service::addTrenchCoat(const string &size, const string &colour, int price, int quantity, const string &photo) {
    TrenchCoat trenchCoat(size, colour, price, quantity, photo);
    if (this->repository.Search(trenchCoat))
        throw runtime_error("Trench coat already exists!");
    this->repository.Add(trenchCoat);
}

void Service::removeTrenchCoat(const string &size, const string &colour) {
    for (int i = 0; i < this->repository.GetSize(); i++) {
        TrenchCoat &currentTrenchCoat = this->repository[i];
        if (currentTrenchCoat.GetSize() == size && currentTrenchCoat.GetColor() == colour) {
            this->repository.Remove(i);
            return;
        }
    }
    throw runtime_error("Trench coat not found!");
}

void Service::updateTrenchCoat(const string &size, const string &colour, int newPrice, int newQuantity, const string &newPhoto) {
    for (int i = 0; i < this->repository.GetSize(); i++) {
        TrenchCoat &currentTrenchCoat = this->repository[i];
        if (currentTrenchCoat.GetSize() == size && currentTrenchCoat.GetColor() == colour) {
            currentTrenchCoat.SetPrice(newPrice);
            currentTrenchCoat.SetQuantity(newQuantity);
            currentTrenchCoat.SetPhotograph(newPhoto);
            return;
        }
    }
    throw runtime_error("Trench coat not found!");
}

DynamicVector<TrenchCoat> Service::getAllTrenchCoats() {
    return this->repository.GetAll();
}
