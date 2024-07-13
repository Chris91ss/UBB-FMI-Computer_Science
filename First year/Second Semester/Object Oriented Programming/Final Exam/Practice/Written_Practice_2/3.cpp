#include <iostream>
#include <vector>
using namespace std;

class Action {
public:
    virtual void execute() = 0;
};

class CreateAction: public Action {
public:
    void execute() override {
        cout << "Create file" << endl;
    }
};

class ExitAction: public Action {
public:
    void execute() override {
        cout << "Exit application" << endl;
    }
};

class MenuItem {
private:
    Action *action;
    string text;
public:
    MenuItem(Action *action = nullptr, string text = ""): action(action), text(text) {}
    ~MenuItem() {
        delete action;
    }
    virtual void print() {
        cout << text << endl;
    }

    void clicked(){
        cout << text << endl;
        action->execute();
    }
};


class Menu: public MenuItem{
private:
    vector<MenuItem> actions;
public:
    Menu(string text): MenuItem(nullptr, text) {}
    void add(MenuItem &item) {
        actions.push_back(item);
    }

    void print() override{
        MenuItem::print();
        for (auto &item: actions) {
            item.print();
        }
    }
};

class MenuBar {
private:
    vector<Menu> menus;
public:
    void add(Menu &item) {
        menus.push_back(item);
    }

    void print() {
        for (auto &item : menus) {
            item.print();
        }
    }
};

int main() {
    // Create MenuBar
    MenuBar menuBar;

    // Create Menus
    Menu fileMenu("File");
    Menu aboutMenu("About");

    // Create submenus and items
    Menu newMenu("New");
    MenuItem textItem(new CreateAction(), "Text");
    MenuItem cppItem(new CreateAction(), "C++");
    newMenu.add(textItem);
    newMenu.add(cppItem);

    MenuItem exitItem(new ExitAction(), "Exit");

    // Add items to File menu
    fileMenu.add(newMenu);
    fileMenu.add(exitItem);

    // Add Menus to MenuBar
    menuBar.add(fileMenu);
    menuBar.add(aboutMenu);

    // Print MenuBar
    menuBar.print();

    // Simulate clicks
    cout << "Simulating clicks:" << endl;
    fileMenu.clicked();
    newMenu.clicked();
    cppItem.clicked();
    exitItem.clicked();

    return 0;
}