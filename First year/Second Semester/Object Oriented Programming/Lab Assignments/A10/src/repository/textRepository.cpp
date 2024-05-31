#include "../../headers/repository/textRepository.h"

TextRepository::TextRepository(const string &fileName) : fileName(fileName) {}

TextRepository::TextRepository() = default;

void TextRepository::Add(const TrenchCoat &trenchCoat) {
    Repository::Add(trenchCoat);
    WriteToFile();
}

void TextRepository::Remove(int index) {
    Repository::Remove(index);
    WriteToFile();
}

void TextRepository::RemoveByValue(const TrenchCoat &trenchCoat) {
    Repository::RemoveByValue(trenchCoat);
    WriteToFile();
}

void TextRepository::WriteToFile() {
    ofstream file(this->fileName);
    if (!file.is_open()) {
        throw FileException("Could not open file");
    }

    for (auto &elem: this->elements) {
        file << elem;
    }

    file.close();
}

void TextRepository::readFromFile() {
    ifstream file(this->fileName);
    if (!file.is_open()) {
        throw FileException("Could not open file");
    }

    TrenchCoat elem;
    while (file >> elem) {
        this->elements.push_back(elem);
    }

    file.close();
}

