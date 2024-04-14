#include "textRepository.h"

TextRepository::TextRepository(const string &fileName) : fileName(fileName) {}

TextRepository::TextRepository() = default;

void TextRepository::Add(const TrenchCoat &trenchCoat) {
    Repository::Add(trenchCoat);
    writeToFile();
}

void TextRepository::Remove(int index) {
    Repository::Remove(index);
    writeToFile();
}

void TextRepository::RemoveByValue(const TrenchCoat &trenchCoat) {
    Repository::RemoveByValue(trenchCoat);
    writeToFile();
}

void TextRepository::writeToFile() {
    ofstream file(this->fileName);
    if (!file.is_open()) {
        throw exception();
    }


    for (auto &elem: this->elements) {
        file << elem;
    }

    file.close();
}

void TextRepository::readFromFile() {
    ifstream file(this->fileName);
    if (!file.is_open()) {
        throw exception();
    }

    TrenchCoat elem;
    while (file >> elem) {
        this->elements.push_back(elem);
    }

    file.close();
}

