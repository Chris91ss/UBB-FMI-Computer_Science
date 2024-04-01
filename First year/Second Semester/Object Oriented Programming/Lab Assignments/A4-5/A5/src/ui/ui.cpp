#include "../../headers/ui/ui.h"

UI::UI(const Service &service, const Service &shoppingBasketService): service(service), shoppingBasketService(shoppingBasketService) {
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
    cout << "1. Cycle through the trench coats having a given size" << endl;
    cout << "2. See the shopping basket" << endl;
    cout << "3. Empty the shopping basket" << endl;
    cout << "0. Back" << endl;
}

void UI::RunUser() {
    int option;
    while (true) {
        UI::PrintUserMenu();

        option = UI::GetOption();

        try {
            switch (option) {
                case 1: {
                    CycleThroughTrenchCoats();
                    break;
                }
                case 2: {
                    SeeShoppingBasket();
                    break;
                }
                case 3: {
                    EmptyShoppingBasket();
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

void UI::AddTrenchCoat() {
    string size, color, photo;
    int quantity;
    double price;
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
    double price;
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

void UI::CycleThroughTrenchCoats() {
    string getSize;
    int option;
    cout << ">Size:";
    cin >> getSize;

    DynamicVector<TrenchCoat> filteredTrenchCoats = this->service.getFilteredBySizeTrenchCoats(getSize);
    if(filteredTrenchCoats.GetSizeOfDynamicVector() == 0) {
        cout << ">No trench coats with the given size!" << endl;
        return;
    }

    int index = 0;
    while(index < filteredTrenchCoats.GetSizeOfDynamicVector()) {
        cout << ">>>>>>>> Total price:" << this->shoppingBasketService.getTotalBasketPrice() << " <<<<<<<<\n" << endl;
        TrenchCoat &trenchCoat = filteredTrenchCoats[index];

        if(trenchCoat.GetQuantity() == 0) {
            filteredTrenchCoats.RemoveFromDynamicVector(index);
            if(filteredTrenchCoats.GetSizeOfDynamicVector() == 0) {
                cout << ">No more trench coats with the given size!" << endl;
                return;
            }
        }

        cout << ">Size:" << trenchCoat.GetSize() << endl
        << " Color:" << trenchCoat.GetColor() << endl
        << " Price:" << trenchCoat.GetPrice() << endl
        << " Quantity:" << trenchCoat.GetQuantity() << endl
        << " Photo:" << trenchCoat.GetPhotograph() << endl << endl;

        index++;
        if(index == filteredTrenchCoats.GetSizeOfDynamicVector())
            index = 0;

        try {
            ShoppingBasketMenu();

            option = UI::GetOption();
            switch (option) {
                case 1: {
                    int quantity = AddToShoppingBasket(trenchCoat);
                    filteredTrenchCoats[index - 1].SetQuantity(filteredTrenchCoats[index - 1].GetQuantity() - quantity);
                    break;
                }
                case 2: {
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

void UI::SeeShoppingBasket() {
    DynamicVector<TrenchCoat> trenchCoats = this->shoppingBasketService.getAllTrenchCoats();
    cout << ">>>>>>>> Total price:" << this->shoppingBasketService.getTotalBasketPrice() << " <<<<<<<<\n" << endl;
    for (int i = 0; i < trenchCoats.GetSizeOfDynamicVector(); i++) {
        TrenchCoat &trenchCoat = trenchCoats[i];
        cout << ">Size:" << trenchCoat.GetSize() << endl
        << " Color:" << trenchCoat.GetColor() << endl
        << " Price:" << trenchCoat.GetPrice() << endl
        << " Quantity:" << trenchCoat.GetQuantity() << endl
        << " Photo:" << trenchCoat.GetPhotograph() << endl << endl;
    }
}

void UI::ShoppingBasketMenu() {
    cout << "1. Add to shopping basket" << endl;
    cout << "2. Don't add to shopping basket and go to the next item" << endl;
    cout << "0. Back" << endl;
}

int UI::AddToShoppingBasket(const TrenchCoat& trenchCoat) {
    int quantity = 0;
    cout << ">Quantity:";
    while (!(cin >> quantity) || quantity > trenchCoat.GetQuantity()) {
        cout << "\n>Invalid input! Number must be lower or equal to the available quantity" << endl;
        cout << ">Quantity:";
        cin.clear();
        cin.ignore(1000, '\n');
    }

    int quantityInBasket = 0;
    DynamicVector<TrenchCoat> shoppingTrenchCoats = this->shoppingBasketService.getAllTrenchCoats();
    for(int i = 0; i < shoppingTrenchCoats.GetSizeOfDynamicVector(); i++) {
        TrenchCoat &currentTrenchCoat = shoppingTrenchCoats[i];
        if (shoppingTrenchCoats.SearchInDynamicVector(trenchCoat))
            quantityInBasket += currentTrenchCoat.GetQuantity();
    }

    if(!shoppingBasketService.searchTrenchCoat(trenchCoat)) {
        this->shoppingBasketService.addTrenchCoat(trenchCoat.GetSize(), trenchCoat.GetColor(),
                                                  trenchCoat.GetPrice(), quantity, trenchCoat.GetPhotograph());
        cout << ">Trench coat added to the shopping basket!" << endl;
    }
    else
    {
        this->shoppingBasketService.updateTrenchCoat(trenchCoat.GetSize(), trenchCoat.GetColor(),
                                                     trenchCoat.GetPrice(),
                                                     quantityInBasket + quantity,
                                                     trenchCoat.GetPhotograph());
        cout << ">Trench coat updated in the shopping basket!" << endl;
    }
    this->shoppingBasketService.setTotalBasketPrice(this->shoppingBasketService.getTotalBasketPrice() + (trenchCoat.GetPrice() * quantity));
    return quantity;
}

void UI::EmptyShoppingBasket() {
    DynamicVector<TrenchCoat> trenchCoats = this->shoppingBasketService.getAllTrenchCoats();
    for(int i = 0; i < this->shoppingBasketService.getAllTrenchCoats().GetSizeOfDynamicVector(); i++) {
        this->shoppingBasketService.removeTrenchCoat(trenchCoats[i].GetSize(), trenchCoats[i].GetColor());
    }
    this->shoppingBasketService.setTotalBasketPrice(0);
    cout << ">Shopping basket emptied!" << endl;
}



