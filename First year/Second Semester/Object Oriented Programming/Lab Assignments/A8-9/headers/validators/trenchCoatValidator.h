#pragma once
#include "../../headers/domain/trenchCoat.h"


class TrenchCoatException : public exception {
private:
    vector<string> errors;

public:
        /// Constructor for a TrenchCoatException.
        /// \param errors - vector of strings, the errors
        explicit TrenchCoatException(vector<string> errors);

        /// Getter for the errors.
        vector<string> getErrors() const;
};

class TrenchCoatValidator {
public:

        /// Default constructor for a TrenchCoatValidator.
        TrenchCoatValidator() = default;

        /// Validates a trench coat.
        /// \param trenchCoat - TrenchCoat, the trench coat to be validated
        /// \throws TrenchCoatException - if the trench coat is invalid
        static void validate(const TrenchCoat &trenchCoat);
        static bool validateSize(const string &size);
        static bool validateColor(const string &color);
};

