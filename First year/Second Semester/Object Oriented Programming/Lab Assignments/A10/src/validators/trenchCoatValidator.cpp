#include <utility>

#include "../../headers/validators/trenchCoatValidator.h"

TrenchCoatException::TrenchCoatException(vector <string> errors) {
    this->errors = std::move(errors);
}

vector<string> TrenchCoatException::getErrors() const {
    return this->errors;
}

void TrenchCoatValidator::validate(const TrenchCoat &trenchCoat) {
    vector<string> errors;

    if (trenchCoat.GetSize().empty()) {
        errors.emplace_back("The size cannot be empty!");
    }
    if (trenchCoat.GetColor().empty()) {
        errors.emplace_back("The color cannot be empty!");
    }
    if (trenchCoat.GetPrice() < 0) {
        errors.emplace_back("The price cannot be negative!");
    }
    if (trenchCoat.GetQuantity() < 0) {
        errors.emplace_back("The quantity cannot be negative!");
    }
    if (trenchCoat.GetPhotograph().empty()) {
        errors.emplace_back("The photo cannot be empty!");
    }
    if (!validateSize(trenchCoat.GetSize())) {
        errors.emplace_back("The size is invalid!");
    }
    if (!validateColor(trenchCoat.GetColor())) {
        errors.emplace_back("The color is invalid!");
    }


    if (!errors.empty()) {
        throw TrenchCoatException(errors);
    }
}

bool TrenchCoatValidator::validateSize(const string &size) {
    if (size == "XXS" || size == "XS" || size == "S" || size == "M" || size == "L" || size == "XL" || size == "XXL" || size == "XXXL") {
        return true;
    }
    return false;
}

bool TrenchCoatValidator::validateColor(const string &color) {
    try {
        int check = stoi(color);
    } catch (exception &exception) {
        return true;
    }
    return false;
}
