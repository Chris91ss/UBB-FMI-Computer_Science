#include "ui/ui.h"

UI::UI(const Service &service) : service(service) {
    this->service.Generate5Bills();
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
                        addBillUI();
                        break;
                    case 2:
                        removeBillUI();
                        break;
                    case 3:
                        GetAllBillsUI();
                        break;
                    case 4:
                        GetAllUnpaidBillsUI();
                        break;
                    case 5:
                        CalculateTotalAmountOfUnpaidBillsUI();
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
    cout << "1. Add bill" << endl;
    cout << "2. Remove bill" << endl;
    cout << "3. Display all bills" << endl;
    cout << "4. Sort unpaid bills by due date" << endl;
    cout << "5. Calculate total amount of unpaid bills" << endl;
}

void UI::addBillUI() {
    string serialNumber, company;
    double sum;
    bool isPaid;
    DateTime dueDate;
    cout << "Enter serial number: ";
    cin >> serialNumber;
    cout << "Enter company: ";
    cin >> company;
    cout << "Enter due date: ";
    cout << "Day Month Year" << endl;
    cin >> dueDate.day >> dueDate.month >> dueDate.year;
    cout << "Enter sum: ";
    cin >> sum;
    cout << "Is paid? (1/0): ";
    cin >> isPaid;
    this->service.addBill(Bill(serialNumber, company, dueDate, sum, isPaid));

    cout << "Bill added successfully!" << endl;
}

void UI::removeBillUI() {
    string serialNumber;
    cout << "Enter serial number: ";
    cin >> serialNumber;
    this->service.removeBill(serialNumber);

    cout << "Bill removed successfully!" << endl;
}

void UI::GetAllBillsUI() {
    DynamicVector<Bill> bills = this->service.getAllBills();
    for (int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        Bill bill = bills[i];
        cout << bill.getSerialNumber() << " - " << bill.getCompany() << " - " << bill.getDueDate() << " - " << bill.getSum() << " - " << bill.getIsPaid() << endl;
    }
}

void UI::GetAllUnpaidBillsUI() {
    DynamicVector<Bill> bills = this->service.sortAllUnpaidBillsByDueDate();
    for (int i = 0; i < bills.GetSizeOfDynamicVector(); i++) {
        Bill bill = bills[i];
        cout << bill.getSerialNumber() << " - " << bill.getCompany() << " - " << bill.getDueDate() << " - " << bill.getSum() << " - " << bill.getIsPaid() << endl;
    }
}

void UI::CalculateTotalAmountOfUnpaidBillsUI() {
    double totalAmount = this->service.calculateTotalAmountOfUnpaidBills();
    cout << "Total amount of unpaid bills: " << totalAmount << endl;
}
