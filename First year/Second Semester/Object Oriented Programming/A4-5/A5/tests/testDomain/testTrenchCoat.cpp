#include "testTrenchCoat.h"

void TestTrenchCoat::testAllTrenchCoat() {
    testTrenchCoatConstructors();
    testTrenchCoatOperator();
    testTrenchCoatGetters();
    testTrenchCoatSetters();
}

void TestTrenchCoat::testTrenchCoatConstructors() {
    TrenchCoat trenchCoat;
    assert(trenchCoat.GetSize().empty());
    assert(trenchCoat.GetColor().empty());
    assert(trenchCoat.GetPrice() == 0);
    assert(trenchCoat.GetQuantity() == 0);
    assert(trenchCoat.GetPhotograph().empty());


    TrenchCoat trenchCoat1("M", "Black", 100, 10, "photo");
    assert(trenchCoat1.GetSize() == "M");
    assert(trenchCoat1.GetColor() == "Black");
    assert(trenchCoat1.GetPrice() == 100);
    assert(trenchCoat1.GetQuantity() == 10);
    assert(trenchCoat1.GetPhotograph() == "photo");
}

void TestTrenchCoat::testTrenchCoatOperator() {
    TrenchCoat trenchCoat("M", "Black", 100, 10, "photo");
    TrenchCoat trenchCoat1 = trenchCoat;
    assert(trenchCoat1.GetSize() == "M");
    assert(trenchCoat1.GetColor() == "Black");
    assert(trenchCoat1.GetPrice() == 100);
    assert(trenchCoat1.GetQuantity() == 10);
    assert(trenchCoat1.GetPhotograph() == "photo");

    assert(trenchCoat == trenchCoat1);
}

void TestTrenchCoat::testTrenchCoatGetters() {
    TrenchCoat trenchCoat("M", "Black", 100, 10, "photo");
    assert(trenchCoat.GetSize() == "M");
    assert(trenchCoat.GetColor() == "Black");
    assert(trenchCoat.GetPrice() == 100);
    assert(trenchCoat.GetQuantity() == 10);
    assert(trenchCoat.GetPhotograph() == "photo");
}

void TestTrenchCoat::testTrenchCoatSetters() {
    TrenchCoat trenchCoat("M", "Black", 500, 23, "Image");
    trenchCoat.SetPrice(100);
    trenchCoat.SetQuantity(10);
    trenchCoat.SetPhotograph("photo");
    assert(trenchCoat.GetSize() == "M");
    assert(trenchCoat.GetColor() == "Black");
    assert(trenchCoat.GetPrice() == 100);
    assert(trenchCoat.GetQuantity() == 10);
    assert(trenchCoat.GetPhotograph() == "photo");
}
