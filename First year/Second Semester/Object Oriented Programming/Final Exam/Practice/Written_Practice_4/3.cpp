#include <iostream>
#include <vector>
#include <memory>
using namespace std;

// SaleItem class
class SaleItem {
public:
    int code;
    double price;

    SaleItem(int c, double p) : code(c), price(p) {}
};

// Sale class
class Sale {
public:
    vector<SaleItem> items;

    void addItem(int code, double price) {
        items.emplace_back(code, price);
    }
};

// Abstract Discount class
class Discount {
public:
    virtual double calc(const Sale& sale) const = 0;
    virtual ~Discount() = default;
};

// ItemDiscount class
class ItemDiscount : public Discount {
private:
    int code;
    double percentage;
public:
    ItemDiscount(int c, double p) : code(c), percentage(p) {}

    double calc(const Sale& sale) const override {
        double discount = 0.0;
        for (const auto& item : sale.items) {
            if (item.code == code) {
                discount += item.price * (percentage / 100.0);
            }
        }
        return discount;
    }
};

// SumDiscount class
class SumDiscount : public Discount {
private:
    vector<shared_ptr<Discount>> discounts;
public:
    void add(shared_ptr<Discount> discount) {
        discounts.push_back(discount);
    }

    double calc(const Sale& sale) const override {
        double totalDiscount = 0.0;
        for (const auto& discount : discounts) {
            totalDiscount += discount->calc(sale);
        }
        return totalDiscount;
    }
};

int main() {
    // Create a sale with 3 items
    Sale sale;
    sale.addItem(1, 100.0);
    sale.addItem(2, 150.0);
    sale.addItem(1, 200.0);

    // Create discounts
    auto discount1 = make_shared<ItemDiscount>(1, 10.0); // 10% discount on code 1
    auto discount2 = make_shared<ItemDiscount>(2, 15.0); // 15% discount on code 2

    // Create a SumDiscount and add the discounts
    SumDiscount sumDiscount;
    sumDiscount.add(discount1);
    sumDiscount.add(discount2);

    // Calculate the total discount for the sale
    double totalDiscount = sumDiscount.calc(sale);
    cout << "Total discount: " << totalDiscount << endl;

    return 0;
}
