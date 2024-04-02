
#include "ui/ui.h"

UI::UI(const Service &service) : service(service) {
    this->service.Generate5BillsAtStartup();
}

UI::~UI() = default;

void UI::run() {
    int option;
    try
    {
        while (true)
        {
            printMenu();
            cout << "Option: ";
            cin >> option;
            cin.ignore();
            try {
                switch (option) {
                    case 1:
                        addBillUI();
                        break;
                    case 2:
                        getAllBillsUI();
                        break;
                    case 3:
                        getAllBillsSortedUI();
                        break;
                    case 4:
                        getAllPaidBillsUI();
                        break;
                    case 0:
                        exitApp();
                        return;
                    default:
                        cout << "Invalid option!\n";
                        break;
                }
            }
            catch (exception &exception) {
                cout << exception.what() << '\n';
            }
        }
    }
    catch (exception &exception)
    {
        cout << exception.what() << '\n';

    }
}

void UI::printMenu() {
    cout << "1. Add bill\n";
    cout << "2. Display all bills\n";
    cout << "3. Display all bills sorted by company name\n";
    cout << "4. Show all paid bills and calculate their total amount\n";
    cout << "0. Exit\n";
}

void UI::addBillUI() {
    string company, serialNumber;
    double sum;
    bool isPaid;
    cout << "Enter company: ";
    getline(cin, company);
    cout << "Enter serial number: ";
    getline(cin, serialNumber);
    cout << "Enter sum: ";
    cin >> sum;
    cout << "Is paid? (1/0): ";
    cin >> isPaid;
    this->service.addBill(Bill(company, serialNumber, sum, isPaid));
    cout << "Bill added successfully!\n";
}

void UI::getAllBillsUI() {
    DynamicVector<Bill> bills = this->service.getAllBills();
    for (int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        cout << bills[i].getCompanyName() << "; " << bills[i].getSerialNumber() << "; "
        << bills[i].getSum() << "; " << bills[i].getIsPaid() << '\n';
    }
}

void UI::getAllBillsSortedUI() {
    DynamicVector<Bill> bills = this->service.getAllBillsSortedByCompanyName();
    for (int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        cout << bills[i].getCompanyName() << "; " << bills[i].getSerialNumber() << "; "
        << bills[i].getSum() << "; " << bills[i].getIsPaid() << '\n';
    }
}

void UI::getAllPaidBillsUI() {
    double sum;
    DynamicVector<Bill> bills = this->service.getAllPaidBillsAndTheirSum(sum);
    for (int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        cout << bills[i].getCompanyName() << "; " << bills[i].getSerialNumber() << "; "
        << bills[i].getSum() << "; " << bills[i].getIsPaid() << '\n';
    }
    cout << "Total amount of paid bills: " << sum << '\n';
}

void UI::exitApp() {
    cout << "Exiting...\n";
    exit(0);
}
