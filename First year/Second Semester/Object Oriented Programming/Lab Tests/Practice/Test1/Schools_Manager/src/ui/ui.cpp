
#include "ui/ui.h"

UI::UI(const Service &service) : service(service) {
    this->service.Generate5Schools();
}

UI::~UI() = default;

void UI::run() {
    int option;
    try {
        while (true) {
            printMenu();
            cout << "Choose an option: ";
            cin >> option;
            try {
                switch (option) {
                    case 1:
                        addSchoolUI();
                        break;
                    case 2:
                        removeSchoolUI();
                        break;
                    case 3:
                        GetAllSchoolsUI();
                        break;
                    case 4:
                        GetAllSchoolsSortedUI();
                        break;
                    case 5:
                        GetAllSchoolsAfterAGivenDateUI();
                        break;
                    default:
                        cout << "Invalid option!" << endl;
                }
            }
            catch (exception &exception) {
                cout << exception.what() << endl;
            }
        }
    }
    catch (exception &exception) {
        cout << exception.what() << endl;
    }
}

void UI::printMenu() {
    cout << "1. Add school" << endl;
    cout << "2. Remove school" << endl;
    cout << "3. Display all schools" << endl;
    cout << "4. Display all schools sorted by name" << endl;
    cout << "5. Display all schools after a given date" << endl;
}

void UI::addSchoolUI() {
    string name;
    Location location;
    DateTime dateToVisit;
    int aux;
    cout << "Enter name: ";
    cin >> name;
    cout << "Enter location: ";
    cout << "Enter latitude: ";
    cin >> aux;
    location.setLatitude(aux);
    cout << "Enter longitude: ";
    cin >> aux;
    location.setLongitude(aux);
    cout << "Enter date to visit: ";
    cout << "Enter day: ";
    cin >> aux;
    dateToVisit.setDay(aux);
    cout << "Enter month: ";
    cin >> aux;
    dateToVisit.setMonth(aux);
    cout << "Enter year: ";
    cin >> aux;
    dateToVisit.setYear(aux);
    bool isVisited;
    cout << "Was the school visited? (1 - yes, 0 - no)";
    cin >> isVisited;
    this->service.addSchool(School(name, location, dateToVisit, isVisited));
}

void UI::removeSchoolUI() {
    string name;
    cout << "Enter name: ";
    cin >> name;
    this->service.removeSchool(name);
}

void UI::GetAllSchoolsUI() {
    DynamicVector<School> schools = this->service.getAllSchools();
    for (int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        cout << schools[i].getName() << " | " << schools[i].getLocation().getLongitude() << " | " << schools[i].getLocation().getLatitude() << " | "
        << schools[i].getDateOfVisit() << " | " << schools[i].getWasVisited() << endl;
    }
}

void UI::GetAllSchoolsSortedUI() {
    DynamicVector<School> schools = this->service.getAllSchoolsSortedByName();
    for (int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        cout << schools[i].getName() << " | " << schools[i].getLocation().getLongitude() << " | " << schools[i].getLocation().getLatitude() << " | "
        << schools[i].getDateOfVisit() << " | " << schools[i].getWasVisited() << endl;
    }
}

void UI::GetAllSchoolsAfterAGivenDateUI() {
    DateTime date;
    int aux;
    cout << "Enter date: \n";
    cout << "Enter day: ";
    cin >> aux;
    date.setDay(aux);
    cout << "Enter month: ";
    cin >> aux;
    date.setMonth(aux);
    cout << "Enter year: ";
    cin >> aux;
    date.setYear(aux);
    DynamicVector<School> schools = this->service.getAllSchoolsAfterAGivenDate(date);
    for (int i = 0; i < schools.GetSizeOfDynamicVector(); i++) {
        cout << schools[i].getName() << " | " << schools[i].getLocation().getLongitude() << " | " << schools[i].getLocation().getLatitude() << " | "
        << schools[i].getDateOfVisit() << " | " << schools[i].getWasVisited() << endl;
    }
}
