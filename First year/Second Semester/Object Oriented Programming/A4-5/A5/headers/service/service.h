#pragma once
#include "../domain/trenchCoat.h"
#include "../repository/repository.h"

class Service {
private:
    Repository<TrenchCoat> repository;

public:
    explicit Service(const Repository<TrenchCoat>& repository);
    Service(const Service &other);
    ~Service();
    Service &operator=(const Service &other);

    void Generate10Entities();

    void addTrenchCoat(string const &size, string const &colour, double price, int quantity, string const &photo);
    void removeTrenchCoat(string const &size, string const &colour);
    void updateTrenchCoat(string const &size, string const &colour, double newPrice, int newQuantity, string const &newPhoto);
    bool searchTrenchCoat(const TrenchCoat &trenchCoat) const;
    DynamicVector<TrenchCoat> getAllTrenchCoats();
    DynamicVector<TrenchCoat> getFilteredBySizeTrenchCoats(string const &size);
    double getTotalBasketPrice() const;
    void setTotalBasketPrice(double newTotalBasketPrice);
};