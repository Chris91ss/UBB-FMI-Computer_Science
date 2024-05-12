#include "../../headers/repository/htmlRepository.h"
//#include <Windows.h>
#include <regex>

HTMLRepository::HTMLRepository(string fileName) : fileName(std::move(fileName)) {}

void HTMLRepository::Add(const TrenchCoat &trenchCoat) {
    Repository::Add(trenchCoat);
    this->WriteToFile();
}

void HTMLRepository::WriteToFile() {
    ofstream file(this->fileName.c_str());
    if (!file.is_open()) {
        throw FileException("Could not open file");
    }

    file << R"(<!DOCTYPE html>)" << endl;
    file << R"(<html>)" << endl;
    file << R"(<head>)" << endl;
    file << R"(<title>Shopping Basket</title>)" << endl;
    file << R"(</head>)" << endl;
    file << R"(<body>)" << endl;
    file << R"(<table border="1">)" << endl;
    file << R"(<tr>)" << endl;
    file << R"(<th>Size</th>)" << endl;
    file << R"(<th>Color</th>)" << endl;
    file << R"(<th>Price</th>)" << endl;
    file << R"(<th>Quantity</th>)" << endl;
    file << R"(<th>Photo</th>)" << endl;
    file << R"(</tr>)" << endl;

    for (const auto &trenchCoat: this->GetAll()) {
        file << R"(<tr>)" << endl;
        file << R"(<td>)" << trenchCoat.GetSize() << R"(</td>)" << endl;
        file << R"(<td>)" << trenchCoat.GetColor() << R"(</td>)" << endl;
        file << R"(<td>)" << trenchCoat.GetPrice() << R"(</td>)" << endl;
        file << R"(<td>)" << trenchCoat.GetQuantity() << R"(</td>)" << endl;
        file << R"(<td><a href=")" << trenchCoat.GetPhotograph() << R"(">Link</a></td>)" << endl;
        file << R"(</tr>)" << endl;
    }

    file << R"(</table>)" << std::endl;
    file << R"(</body>)" << std::endl;
    file << R"(</html>)" << std::endl;

    file.close();
}

void HTMLRepository::ReadFromFile() {
    ifstream HTMLInputFile(this->fileName.c_str());

    if (!HTMLInputFile.is_open())
        throw FileException("The HTML file could not be opened!");

    std::string line;
    std::string html_content;
    while (getline(HTMLInputFile, line)) {
        html_content += line + "\n";
    }

    regex row_pattern(R"lit(<tr>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>\s*<td><a href="([^"]*)">[^<]*</a></td>\s*</tr>)lit");
    smatch match;

    while (std::regex_search(html_content, match, row_pattern) && match.size() > 5) {
        string size = match.str(1);
        string color = match.str(2);
        string price = match.str(3);
        string quantity = match.str(4);
        string photo = match.str(5);

        TrenchCoat trenchCoat(size, color, stod(price), stoi(quantity), photo);
        Repository::Add(trenchCoat);

        html_content = match.suffix().str();
    }

    HTMLInputFile.close();
}

void HTMLRepository::OpenInApplication() {
    cout << "Opening in browser...";
}



