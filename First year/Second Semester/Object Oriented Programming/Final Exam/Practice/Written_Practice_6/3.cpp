#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Icecream {
public:
    virtual string getDescription() const = 0;
    virtual double computePrice() const = 0;
    virtual ~Icecream() {}
};

class SimpleIcecream : public Icecream {
private:
    string description;
    double price;
public:
    SimpleIcecream(const string& desc, double pr) : description(desc), price(pr) {}
    string getDescription() const override {
        return "simple ice cream with " + description;
    }
    double computePrice() const override {
        return price;
    }
};

class IcecreamWithTopping : public Icecream {
protected:
    Icecream* baseIcecream;
public:
    IcecreamWithTopping(Icecream* base) : baseIcecream(base) {}
    virtual string addTopping() const = 0;
    string getDescription() const override {
        return baseIcecream->getDescription() + " " + addTopping();
    }
    virtual ~IcecreamWithTopping() {
        delete baseIcecream;
    }
};

class IcecreamWithChocolateTopping : public IcecreamWithTopping {
public:
    IcecreamWithChocolateTopping(Icecream* base) : IcecreamWithTopping(base) {}
    string addTopping() const override {
        return "with chocolate topping";
    }
    double computePrice() const override {
        return baseIcecream->computePrice() + 3;
    }
};

class IcecreamWithCaramelTopping : public IcecreamWithTopping {
public:
    IcecreamWithCaramelTopping(Icecream* base) : IcecreamWithTopping(base) {}
    string addTopping() const override {
        return "with caramel topping";
    }
    double computePrice() const override {
        return baseIcecream->computePrice() + 2;
    }
};

class Order {
private:
    vector<Icecream*> icecreams;
public:
    void addIcecream(Icecream* icecream) {
        icecreams.push_back(icecream);
    }
    void printOrder() const {
        vector<Icecream*> sortedIcecreams = icecreams;
        sort(sortedIcecreams.begin(), sortedIcecreams.end(), [](Icecream* a, Icecream* b) {
            return a->computePrice() > b->computePrice();
        });
        for (const auto& icecream : sortedIcecreams) {
            cout << icecream->getDescription() << ": " << icecream->computePrice() << " RON" << endl;
        }
    }
    ~Order() {
        for (auto& icecream : icecreams) {
            delete icecream;
        }
    }
};

// int main() {
//     // Create the order
//     Order order;
//
//     // Adding ice creams to the order
//     order.addIcecream(new SimpleIcecream("vanilla", 5.0));
//     order.addIcecream(new IcecreamWithChocolateTopping(new IcecreamWithCaramelTopping(new SimpleIcecream("pistachio", 6.0))));
//     order.addIcecream(new IcecreamWithCaramelTopping(new SimpleIcecream("chocolate", 4.0)));
//     order.addIcecream(new SimpleIcecream("hazelnuts", 5.5));
//
//     // Print the order
//     order.printOrder();
//
//     return 0;
// }
