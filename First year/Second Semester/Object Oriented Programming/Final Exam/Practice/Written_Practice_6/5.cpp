#include <iostream>
#include <string>
#include <memory>

using namespace std;

// Abstract class Handrail
class Handrail {
public:
    virtual double computePrice() const = 0; // Pure virtual function
    virtual ~Handrail() = default; // Virtual destructor
};

// Class WoodHandrail
class WoodHandrail : public Handrail {
public:
    double computePrice() const override {
        return 2.0;
    }
};

// Class MetalHandrail
class MetalHandrail : public Handrail {
public:
    double computePrice() const override {
        return 2.5;
    }
};

// Class HandrailWithVerticalElements
class HandrailWithVerticalElements : public Handrail {
private:
    shared_ptr<Handrail> handrail;
    int noElements;
public:
    HandrailWithVerticalElements(shared_ptr<Handrail> h, int elements)
        : handrail(h), noElements(elements) {}

    double computePrice() const override {
        return handrail->computePrice() + noElements * 5.0;
    }
};

// Abstract class Stair
class Stair {
protected:
    int noSteps;
public:
    Stair(int steps) : noSteps(steps) {}
    virtual double getPrice() const = 0;
    virtual string getDescription() const = 0;
    virtual double getCoefficient() const = 0;
    virtual ~Stair() = default; // Virtual destructor

    int getNoSteps() const { // Getter for noSteps
        return noSteps;
    }
};

// Class WoodStair
class WoodStair : public Stair {
public:
    WoodStair(int steps) : Stair(steps) {}

    double getPrice() const override {
        return getCoefficient() * noSteps;
    }

    string getDescription() const override {
        return "wood stair";
    }

    double getCoefficient() const override {
        return 1.5;
    }
};

// Class MetalStair
class MetalStair : public Stair {
public:
    MetalStair(int steps) : Stair(steps) {}

    double getPrice() const override {
        return getCoefficient() * noSteps;
    }

    string getDescription() const override {
        return "metal stair";
    }

    double getCoefficient() const override {
        return 2.0;
    }
};

// Class StairWithHandrail
class StairWithHandrail : public Stair {
private:
    shared_ptr<Stair> stair;
    shared_ptr<Handrail> handrail;
    double handrailLinearMeters;
public:
    StairWithHandrail(shared_ptr<Stair> s, shared_ptr<Handrail> h, double meters)
        : Stair(s->getNoSteps()), stair(s), handrail(h), handrailLinearMeters(meters) {}

    double getPrice() const override {
        return stair->getPrice() + handrail->computePrice() * handrailLinearMeters;
    }

    string getDescription() const override {
        return stair->getDescription() + " with " + to_string(handrailLinearMeters) + " linear meters of handrail";
    }

    double getCoefficient() const override {
        return 1.0;
    }
};

int main() {
    // Create a simple wood stair with 20 steps
    shared_ptr<Stair> simpleWoodStair = make_shared<WoodStair>(20);

    // Create a metal stair with 10 steps and 5 linear meters of metal handrail
    shared_ptr<Stair> metalStair = make_shared<MetalStair>(10);
    shared_ptr<Handrail> metalHandrail = make_shared<MetalHandrail>();
    shared_ptr<Stair> stairWithMetalHandrail = make_shared<StairWithHandrail>(metalStair, metalHandrail, 5);

    // Create a wood stair with 10 steps, 5 linear meters of wood handrail, and 10 vertical elements
    shared_ptr<Stair> woodStair = make_shared<WoodStair>(10);
    shared_ptr<Handrail> woodHandrail = make_shared<WoodHandrail>();
    shared_ptr<Handrail> woodHandrailWithElements = make_shared<HandrailWithVerticalElements>(woodHandrail, 10);
    shared_ptr<Stair> stairWithWoodHandrail = make_shared<StairWithHandrail>(woodStair, woodHandrailWithElements, 5);

    // Print descriptions and prices
    cout << simpleWoodStair->getDescription() << ": " << simpleWoodStair->getPrice() << endl;
    cout << stairWithMetalHandrail->getDescription() << ": " << stairWithMetalHandrail->getPrice() << endl;
    cout << stairWithWoodHandrail->getDescription() << ": " << stairWithWoodHandrail->getPrice() << endl;

    return 0;
}
