#include "csvRepository.h"

#include <utility>
#include <Windows.h>

CSVRepository::CSVRepository(string fileName) : fileName(std::move(fileName)) {}

void CSVRepository::WriteToFile() {
    ofstream CSVOutputFile(this->fileName.c_str());

    if (!CSVOutputFile.is_open())
        throw FileException("The CSV file could not be opened!");

    CSVOutputFile << "Index, Size, Color, Price, Quantity, Photo\n";
    int index = 0;
    for (const auto& trenchCoat : this->GetAll())
        CSVOutputFile << index++ << ", " << trenchCoat.GetSize() << "," << trenchCoat.GetColor() << ","
                      << trenchCoat.GetPrice() << "," << trenchCoat.GetQuantity() << "," << trenchCoat.GetPhotograph() << "\n";

    CSVOutputFile.close();

}

void CSVRepository::ReadFromFile() {
    ifstream CSVInputFile(this->fileName.c_str());

    if (!CSVInputFile.is_open())
        throw FileException("The CSV file could not be opened!");

    string line;
    getline(CSVInputFile, line);
    while (getline(CSVInputFile, line)) {
        stringstream ss(line);
        string index, size, color, price, quantity, photo;
        getline(ss, index, ',');
        getline(ss, size, ',');
        getline(ss, color, ',');
        getline(ss, price, ',');
        getline(ss, quantity, ',');
        getline(ss, photo, ',');

        TrenchCoat trenchCoat(size, color, stod(price), stoi(quantity), photo);
        this->Add(trenchCoat);
    }

    CSVInputFile.close();
}

void CSVRepository::OpenInApplication() {
    ShellExecuteA(nullptr, nullptr, R"(C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel 2016.lnk)",
                  this->fileName.c_str(), nullptr, SW_SHOWMAXIMIZED);
}



