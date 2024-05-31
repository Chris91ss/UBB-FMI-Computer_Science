#include "../../headers/service/service.h"

Service::Service(Repository &repository) : repository(&repository) {}

Service::~Service() = default;

Service &Service::operator=(const Service &other) {
    if (this == &other)
        return *this;

    this->repository = other.repository;
    return *this;
}

void Service::Generate10Entities() {
    this->addTrenchCoat("S", "Black", 125.99, 2, "https://www.hugoboss.com/ro/en/water-repellent-trench-coat-with-buckled-belt/hbeu50507736_001.html?gad_source=1&gclid=EAIaIQobChMI4cfeoYnlhQMVtphoCR3w5Aa2EAQYAiABEgJbuvD_BwE#zoom");
    this->addTrenchCoat("M", "White", 99.99, 5, "https://www.hugoboss.com/ro/en/oversized-fit-trench-coat-in-water-repellent-cotton/hbeu50505640_357.html?gad_source=1&gclid=EAIaIQobChMIzLe3uYnlhQMV6K2DBx3hCAO-EAQYBCABEgIMmfD_BwE");
    this->addTrenchCoat("L", "Red", 100.99, 7, "https://www.aboutyou.ro/p/influencer/palton-de-primavara-toamna-14112677");
    this->addTrenchCoat("XL", "Blue", 450.99, 1, "https://uk.tommy.com/double-breasted-relaxed-trench-coat-ww0ww41900dw5");
    this->addTrenchCoat("L", "Green", 570.99, 3, "https://eu.akris.com/products/silk-organza-trenchcoat-leaf?gad_source=1&gclid=EAIaIQobChMIjNXQ34rlhQMVmK6DBx1HnQWuEAQYASABEgL4LvD_BwE");
    this->addTrenchCoat("S", "Yellow", 333.99, 5, "https://ro.marinarinaldi.com/p-7011014106001-bolivia-lemon?gad_source=1&gclid=EAIaIQobChMIqLuJ6IrlhQMVmLKDBx02QAPTEAQYBSABEgIKN_D_BwE&gclsrc=aw.ds");
    this->addTrenchCoat("M", "Orange", 999.99, 10, "https://www.aboutyou.ro/p/marikoo/palton-de-primavara-toamna-nanakoo-12504421");
    this->addTrenchCoat("L", "Purple", 128.99, 15, "https://www.aboutyou.ro/p/lauren-ralph-lauren/palton-de-primavara-toamna-14589144");
    this->addTrenchCoat("L", "Pink", 357.99, 11, "https://www.aboutyou.ro/p/lascana/palton-de-vara-16358348");
    this->addTrenchCoat("XXL", "Brown", 246.99, 3, "https://www.hugoboss.com/ro/en/belted-trench-coat-with-hardware-trims/hbeu50521406_220.html?gad_source=1&gclid=EAIaIQobChMIzpqhsIvlhQMVrJaDBx0VhgNpEAQYEiABEgKSfvD_BwE");
}

void Service::addTrenchCoat(const string &size, const string &colour, double price, int quantity, const string &photo) {
    TrenchCoat trenchCoat(size, colour, price, quantity, photo);
    try {
        TrenchCoatValidator::validate(trenchCoat);
    } catch (TrenchCoatException &exception) {
        throw ServiceException("Invalid trench coat data!");
    }

    if (this->repository->Search(trenchCoat))
        throw ServiceException("Trench coat already exists!");
    this->repository->Add(trenchCoat);
}

void Service::removeTrenchCoat(const string &size, const string &colour) {
    for (auto &trenchCoat : this->repository->GetAll()) {
        if (trenchCoat.GetSize() == size && trenchCoat.GetColor() == colour) {
            this->repository->RemoveByValue(trenchCoat);
            return;
        }
    }
    throw ServiceException("Trench coat not found!");
}

void Service::updateTrenchCoat(const string &size, const string &colour, double newPrice, int newQuantity, const string &newPhoto) {
    TrenchCoat newTrenchCoat(size, colour, newPrice, newQuantity, newPhoto);
    try {
        TrenchCoatValidator::validate(newTrenchCoat);
    } catch (TrenchCoatException &exception) {
        throw ServiceException("Invalid trench coat data!");
    }

    for (int i = 0; i < this->repository->GetSize(); i++) {
        TrenchCoat &currentTrenchCoat = (*this->repository)[i];
        if (currentTrenchCoat.GetSize() == size && currentTrenchCoat.GetColor() == colour) {
            currentTrenchCoat.SetPrice(newPrice);
            currentTrenchCoat.SetQuantity(newQuantity);
            currentTrenchCoat.SetPhotograph(newPhoto);
            return;
        }
    }
    throw ServiceException("Trench coat not found!");
}

bool Service::searchTrenchCoat(const TrenchCoat &trenchCoat) const {
    return this->repository->Search(trenchCoat);
}

vector<TrenchCoat> Service::getAllTrenchCoats() {
    return this->repository->GetAll();
}

vector<TrenchCoat> Service::getFilteredBySizeTrenchCoats(string const &size) {
    vector<TrenchCoat> filteredTrenchCoats;
    auto coats = this->repository->GetAll();
    copy_if(coats.begin(), coats.end(),
            back_inserter(filteredTrenchCoats),
            [size](const TrenchCoat &trenchCoat) {
                    return trenchCoat.GetSize() == std::string(size);
            });

    return filteredTrenchCoats;
}

double Service::getTotalBasketPrice() const {
    return this->repository->GetTotalBasketPrice();
}

void Service::setTotalBasketPrice(double newTotalBasketPrice) {
    this->repository->SetTotalBasketPrice(newTotalBasketPrice);
}

void Service::writeShoppingBasketToFile() {
    this->repository->WriteToFile();
}

void Service::openShoppingBasketInApplication() {
    this->repository->OpenInApplication();
}

void Service::setRepository(Repository *newRepository) {
    repository = new Repository(*newRepository);
}

Repository *Service::getRepository() const {
    return new Repository(*repository);
}
