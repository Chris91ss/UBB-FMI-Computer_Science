#include "../../headers/ui/ui.h"

UI::UI(const Service &service): service(service) {
    this->service.Generate10Entities();
}

UI::~UI() = default;

void UI::Run() {
    UI::PrintTitle();

    int option;
    try {
        while (true) {
            cout << "\n1. Admin" << endl;
            cout << "2. User" << endl;
            cout << "0. Exit" << endl;

            option = UI::GetOption();

            if (option == 1)
                this->RunAdmin();
            else if (option == 2)
                this->RunUser();
            else if (option == 0)
                break;
            else
                cout << "Invalid option!" << endl;
        }
    }
    catch (const runtime_error &exception) {
        cout << exception.what() << endl;
    }
}

void UI::PrintTitle() {
    cout << ">|===============================|<" << endl;
    cout << ">|....... Trench Coat Store .....|<" << endl;
    cout << ">|_______________________________|<" << endl;
    cout << ">|...........!Welcome!...........|<" << endl;
    cout << ">|===============================|<" << endl;
}

int UI::GetOption() {
    int option;
    cout << ">Type an option:";

    while (!(cin >> option)) {
        cout << "\n>Invalid input!" << endl;
        cout << ">Type an option:";
        cin.clear();
        cin.ignore(1000, '\n');
    }

    cout << endl;
    return option;
}

void UI::PrintAdminMenu() {
    cout << "1. Add a trench coat" << endl;
    cout << "2. Remove a trench coat" << endl;
    cout << "3. Update a trench coat" << endl;
    cout << "4. Show all trench coats" << endl;
    cout << "0. Back" << endl;
}

void UI::RunAdmin() {
    int option;
    while (true) {
        UI::PrintAdminMenu();

        option = UI::GetOption();

        try {
            switch (option) {
                case 1: {
                    AddTrenchCoat();
                    break;
                }
                case 2: {
                    RemoveTrenchCoat();
                    break;
                }
                case 3: {
                    UpdateTrenchCoat();
                    break;
                }
                case 4: {
                    ListTrenchCoats();
                    break;
                }
                case 0: {
                    return;
                }
                default: {
                    cout << ">Invalid option!" << endl;
                    break;
                }
            }
        }
        catch (const runtime_error &exception) {
            cout << exception.what() << endl;
        }
    }
}

void UI::PrintUserMenu() {
}

void UI::RunUser() {
}

void UI::AddTrenchCoat() {
    string size, color, photo;
    int quantity;
    int price;
    cout << ">Size:";
    cin >> size;
    cout << ">Color:";
    cin >> color;
    cout << ">Price:";
    cin >> price;
    cout << ">Quantity:";
    cin >> quantity;
    cout << ">Photo:";
    cin >> photo;

    this->service.addTrenchCoat(size, color, price, quantity, photo);
}

void UI::RemoveTrenchCoat() {
    string size, color;
    cout << ">Size:";
    cin >> size;
    cout << ">Color:";
    cin >> color;

    try{
        this->service.removeTrenchCoat(size, color);
    }
    catch (const runtime_error &exception){
        cout << exception.what() << endl;
    }
}

void UI::UpdateTrenchCoat() {
    string size, color, photo;
    int quantity;
    int price;
    cout << ">Size:";
    cin >> size;
    cout << ">Color:";
    cin >> color;
    cout << ">Price:";
    cin >> price;
    cout << ">Quantity:";
    cin >> quantity;
    cout << ">Photo:";
    cin >> photo;

    try {
        this->service.updateTrenchCoat(size, color, price, quantity, photo);
    }
    catch (const runtime_error &exception) {
        cout << exception.what() << endl;
    }
}

void UI::ListTrenchCoats() {
    DynamicVector<TrenchCoat> trenchCoats = this->service.getAllTrenchCoats();
    for (int i = 0; i < trenchCoats.GetSizeOfDynamicVector(); i++) {
        TrenchCoat &trenchCoat = trenchCoats[i];
        cout << ">Size:" << trenchCoat.GetSize() << endl
        << " Color:" << trenchCoat.GetColor() << endl
        << " Price:" << trenchCoat.GetPrice() << endl
        << " Quantity:" << trenchCoat.GetQuantity() << endl
        << " Photo:" << trenchCoat.GetPhotograph() << endl << endl;
    }
}
