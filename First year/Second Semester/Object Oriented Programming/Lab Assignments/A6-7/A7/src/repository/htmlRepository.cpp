#include "htmlRepository.h"
#include <Windows.h>

HTMLRepository::HTMLRepository(string fileName) : fileName(std::move(fileName)) {}

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

void HTMLRepository::OpenInApplication() {
    char buffer[MAX_PATH];
    GetFullPathNameA(this->fileName.c_str(), MAX_PATH, buffer, nullptr);
    string absolutePath(buffer);
    replace(absolutePath.begin(), absolutePath.end(), '\\', '/');
    string url = "file:///" + absolutePath;
    string quotedUrl = "\"" + url + "\"";
    ShellExecuteA(nullptr, "open", R"(C:\Program Files\Google\Chrome\Application\chrome.exe)",
                  quotedUrl.c_str(), nullptr, SW_SHOWMAXIMIZED);
}


