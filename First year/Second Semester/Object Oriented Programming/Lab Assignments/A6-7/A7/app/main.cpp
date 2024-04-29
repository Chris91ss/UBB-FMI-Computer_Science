#include <fstream>
#include "ui/ui.h"
#include "test.h"
#include "textRepository.h"
#include "htmlRepository.h"
#include "dataBaseRepository.h"

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

void printTitle()
{
    cout << ">|===============================|<" << endl;
    cout << ">|....... Trench Coat Store .....|<" << endl;
    cout << ">|_______________________________|<" << endl;
    cout << ">|...........!Welcome!...........|<" << endl;
    cout << ">|===============================|<" << endl;
}

int main()
{
    printTitle();

    string repositoryType = getRepositoryType();
    Repository repository;
    TextRepository textRepository("../data/data.txt");
    DataBaseRepository databaseRepository("../data/trenchCoats.db");
    textRepository.readFromFile();
    databaseRepository.readFromFile();

    string shoppingBasketType;
    bool isValid = false;
    cout << "Choose the type of the shopping basket repository (csv, html): ";
    cin >> shoppingBasketType;

    while(!isValid) {
        try {
            if (shoppingBasketType == "csv") {
                isValid = true;
                CSVRepository shoppingBasket("../data/shoppingBasket.csv");
                shoppingBasket.ReadFromFile();
                if (repositoryType == "memory") {
                    Service service(repository);
                    service.Generate10Entities();
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                } else if (repositoryType == "txt") {
                    Service service(textRepository);
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                    textRepository.WriteToFile();
                }
                else if (repositoryType == "database") {
                    Service service(databaseRepository);
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                } else
                    throw RepositoryException("Invalid repository type");
            } else if (shoppingBasketType == "html") {
                isValid = true;
                HTMLRepository shoppingBasket("../data/shoppingBasket.html");
                if (repositoryType == "memory") {
                    Service service(repository);
                    service.Generate10Entities();
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                } else if (repositoryType == "txt") {
                    Service service(textRepository);
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                    textRepository.WriteToFile();
                }
                else if (repositoryType == "database") {
                    Service service(databaseRepository);
                    Service shoppingBasketService(shoppingBasket);
                    UI ui(service, shoppingBasketService);
                    ui.Run();
                }else
                    throw RepositoryException("Invalid repository type");
            } else
                throw RepositoryException("Invalid shopping basket type");
        }
        catch (RepositoryException &exception) {
            cout << exception.what() << endl;
            cout << "Choose the type of the shopping basket repository (csv, html): ";
            cin >> shoppingBasketType;
        }
    }

    Test::TestAll();

    return 0;
}