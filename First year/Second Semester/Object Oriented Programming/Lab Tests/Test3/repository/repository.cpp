#include "repository.h"


void Repository::addDisorder(Disorder *disorder) {
    this->disorders.push_back(disorder);
}

vector<Disorder *> Repository::getDisorders() const {
    return this->disorders;
}

vector<Disorder *> Repository::getDisordersSorted() const {
    vector<Disorder*> sortedDisorders = this->disorders;

    for(int i = 0; i < sortedDisorders.size() - 1; i++) {
        for(int j = i + 1; j < sortedDisorders.size(); j++) {
            if(sortedDisorders[i]->getCategory() > sortedDisorders[j]->getCategory()) {
                Disorder* aux = sortedDisorders[i];
                sortedDisorders[i] = sortedDisorders[j];
                sortedDisorders[j] = aux;
            }
        }
    }

    return sortedDisorders;
}
