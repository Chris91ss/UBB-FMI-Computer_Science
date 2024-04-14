#include <fstream>
#include "ui/ui.h"
#include "test.h"
#include "textRepository.h"

//reads the repository type from a file settings.properties
string getRepositoryType()
{
    ifstream settingsFile("../data/settings.properties");
    if (!settingsFile.is_open())
    {
        ofstream _file("../data/settings.properties");
        _file << "repository=memory";
        _file.close();
        return "memory";
    }

    string line;
    string repositoryType;
    getline(settingsFile, line);
    if (line.find("repository") != string::npos)
    {
        repositoryType = line.substr(line.find('=') + 1);
    }

    settingsFile.close();

    return repositoryType;
}

int main()
{
    string repositoryType = getRepositoryType();
    Repository repository;
    TextRepository textRepository("../data/data.txt");
    textRepository.readFromFile();

    Repository shoppingBasket;
    if(repositoryType == "memory") {
        Service service(repository);
        service.Generate10Entities();
        Service shoppingBasketService(shoppingBasket);
        UI ui(service, shoppingBasketService);
        ui.Run();
    }
    else if(repositoryType == "txt") {
        Service service(textRepository);
        Service shoppingBasketService(shoppingBasket);
        UI ui(service, shoppingBasketService);
        ui.Run();
        textRepository.writeToFile();
    }
    else
        throw runtime_error("Invalid repository type");

    Test::TestAll();

    return 0;
}