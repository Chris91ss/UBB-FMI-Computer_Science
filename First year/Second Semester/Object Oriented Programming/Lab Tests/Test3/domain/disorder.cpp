#include "disorder.h"

#include <utility>

Disorder::Disorder(string category, string name, vector<string> symptoms) {
    this->category = std::move(category);
    this->name = std::move(name);
    this->symptoms = std::move(symptoms);
}

string Disorder::toString() const {
    return category + " " + name;
}

string Disorder::getName() {
    return this->name;
}

string Disorder::getCategory() {
    return this->category;
}

vector<string> Disorder::getSymptoms() const {
    return this->symptoms;
}
