#include "ui.h"

UI::UI(Repository &repo) : repo(repo) {}

void UI::run() {
    while(true)
    {
        printMenu();
        cout << "Enter command: \n";
        int command;
        cin >> command;
        switch(command)
        {
            case 1:
                addAppliance();
                break;
            case 2:
                printAllAppliances();
                break;
            case 3:
                printInefficientAppliances();
                break;
            case 4:
                writeToFile();
                break;
            case 5:
                cout << "Exiting...";
                return;
            default:
                cout << "Invalid command" << endl;
        }

    }
}

void UI::printMenu() {
    cout << "1. Add appliance\n";
    cout << "2. Print all appliances\n";
    cout << "3. Print inefficient appliances\n";
    cout << "4. Write to file\n";
    cout << "5. Exit\n";
}

void UI::addAppliance() {
    int applianceType;
    cout << "Enter appliance type (1 - refrigerator, 2 - washing machine): ";
    cin >> applianceType;
    string id;
    cout << "Enter id: ";
    cin >> id;
    if(applianceType == 1) {
        string electricityUsageClass;
        cout << "Enter electricity usage class (A/A++): ";
        cin >> electricityUsageClass;
        string hasFreezer;
        bool hasFreezerBool;
        cout << "Has freezer? yes/no:";
        cin >> hasFreezer;
        if (hasFreezer == "yes")
            hasFreezerBool = true;
        else if (hasFreezer == "no")
            hasFreezerBool = false;
        else {
            cout << "Invalid input" << endl;
            return;
        }
        repo.addAppliance(new Refrigerator(id, electricityUsageClass, hasFreezerBool));
    }
    else if (applianceType == 2) {
        double consumedElectricity;
        cout << "Enter consumed electricity: ";
        cin >> consumedElectricity;
        repo.addAppliance(new DishWasher(id, consumedElectricity));
    }
    else {
        cout << "Invalid appliance type" << endl;
        return;
    }

    cout << "Appliance has been added \n";
}

void UI::printAllAppliances() const {
    cout << "Appliances are: \n";
    for(auto & appliance : repo.getAllAppliances())
    {
        cout << appliance->toString() << endl;
    }
}

void UI::printInefficientAppliances() const {
    cout << "Inefficient Appliances are: \n";
    for(auto & appliance : repo.getAllWithConsumedElectricityMoreThan(100))
    {
        cout << appliance->toString() << endl;
    }
}

void UI::writeToFile() const {
    string fileName;
    double consumedElectricity;
    cout << "Enter file name: ";
    cin >> fileName;
    cout << "Enter consumed electricity: ";
    cin >> consumedElectricity;
    repo.writeToFile(fileName, consumedElectricity);
    cout << "Data was written to the file " << fileName << "\n";
}

