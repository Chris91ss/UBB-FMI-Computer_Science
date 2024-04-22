
#include "ui.h"
#include "../domain/bmi.h"
#include "../domain/bp.h"

UI::UI(Person& person) : person(person) {}

void UI::run() {
    while(true) {
        printMenu();
        cout << "Enter command: ";
        int command;
        cin >> command;
        clearInput();
        if (command == 7) {
            cout << "Exiting...\n";
            break;
        }
        switch (command) {
            case 1:
                addAnalysis();
                break;
            case 2:
                printAnalyses();
                break;
            case 3:
                printAnalysesByMonth();
                break;
            case 4:
                printIllness();
                break;
            case 5:
                printAnalysesBetweenDates();
                break;
            case 6:
                writeToFile();
                break;
            default:
                cout << "Invalid command\n";
        }
    }
}

void UI::clearInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

void UI::printMenu() {
    cout << "1. Add analysis\n";
    cout << "2. Print analyses\n";
    cout << "3. Print analyses by month\n";
    cout << "4. Print illness\n";
    cout << "5. Print analyses between dates\n";
    cout << "6. Write to file\n";
    cout << "7. Exit\n";
}

void UI::addAnalysis() {
    cout << "Enter the type of the analysis (BMI/BP): ";
    string type;
    cin >> type;
    clearInput();
    cout << "Enter the date of the analysis (yyyy.mm.dd): ";
    string date;
    cin >> date;
    clearInput();
    if(type == "BMI")
    {
        cout << "Enter the value of the analysis: ";
        double value;
        cin >> value;
        clearInput();
        person.addAnalysis(new BMI{date, value});
    }
    else if(type == "BP")
    {
        cout << "Enter the diastolic value and the systolic value: ";
        int diastolic, systolic;
        cin >> diastolic >> systolic;
        clearInput();
        person.addAnalysis(new BP{date, diastolic, systolic});
    }
    else
    {
        cout << "Invalid analysis type\n";
    }
}

void UI::printAnalyses() {
    for(auto* analysis : person.getAllAnalyses())
    {
        cout << analysis->toString() << '\n';
    }
}

void UI::printAnalysesByMonth() {
    cout << "Enter the month: ";
    int month;
    cin >> month;
    clearInput();
    for(auto* analysis : person.getAnalysesByMonth(month))
    {
        cout << analysis->toString() << '\n';
    }
}

void UI::printIllness() {
    cout << "Enter the month: ";
    int month;
    cin >> month;
    clearInput();
    if(person.isIll(month))
    {
        cout << "The person is ill\n";
    }
    else
    {
        cout << "The person is not ill\n";
    }
}

void UI::printAnalysesBetweenDates() {
    cout << "Enter the first date (yyyy.mm.dd): ";
    string date1;
    cin >> date1;
    clearInput();
    cout << "Enter the second date (yyyy.mm.dd): ";
    string date2;
    cin >> date2;
    clearInput();
    for(auto* analysis : person.getAnalysesBetweenDates(date1, date2))
    {
        cout << analysis->toString() << '\n';
    }
}

void UI::writeToFile() {
    cout << "Enter the filename: ";
    string filename;
    cin >> filename;
    clearInput();
    cout << "Enter the first date (yyyy.mm.dd): ";
    string date1;
    cin >> date1;
    clearInput();
    cout << "Enter the second date (yyyy.mm.dd): ";
    string date2;
    cin >> date2;
    clearInput();
    person.writeToFile(filename, date1, date2);
}
