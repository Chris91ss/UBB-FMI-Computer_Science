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

    void addTrenchCoat(string const &size, string const &colour, int price, int quantity, string const &photo);
    void removeTrenchCoat(string const &size, string const &colour);
    void updateTrenchCoat(string const &size, string const &colour, int newPrice, int newQuantity, string const &newPhoto);
    DynamicVector<TrenchCoat> getAllTrenchCoats();

};