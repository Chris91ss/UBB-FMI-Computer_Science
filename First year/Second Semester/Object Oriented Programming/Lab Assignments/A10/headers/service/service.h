#pragma once
#include "../domain/trenchCoat.h"
#include "../repository/repository.h"
#include "../repository/textRepository.h"
#include "../../headers/utilities/exceptions.h"
#include "../../headers/validators/trenchCoatValidator.h"
#include "../../headers/repository/csvRepository.h"
#include "../../headers/repository/htmlRepository.h"

class Service {
private:
    Repository *repository;

public:
    Service() : repository(new TextRepository()) {};
    explicit Service(Repository& repository);
    Service(const Service &other) = default;
    ~Service();
    Service &operator=(const Service &other);

    void Generate10Entities();

    void addTrenchCoat(string const &size, string const &colour, double price, int quantity, string const &photo);
    void removeTrenchCoat(string const &size, string const &colour);
    void updateTrenchCoat(string const &size, string const &colour, double newPrice, int newQuantity, string const &newPhoto);
    bool searchTrenchCoat(const TrenchCoat &trenchCoat) const;
    vector<TrenchCoat> getAllTrenchCoats();
    vector<TrenchCoat> getFilteredBySizeTrenchCoats(string const &size);
    double getTotalBasketPrice() const;
    void setTotalBasketPrice(double newTotalBasketPrice);
    void writeShoppingBasketToFile();
    void openShoppingBasketInApplication();

    void setRepository(Repository *newRepository);
    Repository *getRepository() const;
};

