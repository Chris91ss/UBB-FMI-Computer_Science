//
// Created by qdeni on 6/28/2023.
//

#include "../header_files/Session.h"

using namespace std;

Session::Session(const string &couriersFile, const string &packagesFile) {
    this->couriersFile = couriersFile;
    this->packagesFile = packagesFile;
    this->loadCouriers();
    this->loadPackages();
}

void Session::loadCouriers() {
    ifstream fin(this->couriersFile);
    if (!fin.is_open()) {
        throw runtime_error("Could not open couriers file");
    }

    Courier courier;
    while (fin >> courier) {
        this->couriers.push_back(courier);
        courier.reset();
    }

    fin.close();
}

void Session::loadPackages() {
    ifstream fin(this->packagesFile);
    if (!fin.is_open()) {
        throw runtime_error("Could not open packages file");
    }

    Package package;
    while (fin >> package) {
        this->packages.push_back(package);
    }

    fin.close();
}

void Session::savePackages() {
    ofstream fout(this->packagesFile);
    if (!fout.is_open()) {
        throw runtime_error("Could not open packages file");
    }

    for (const auto &package : this->packages) {
        fout << package << endl;
    }

    fout.close();
}

void Session::addPackage(const string &recipient, const string &street, int number, int x, int y) {
    if (number < 0) {
        throw runtime_error("Invalid package data!");
    }
    if (recipient.empty() || street.empty()) {
        throw runtime_error("Invalid package data!");
    }

    Package package(recipient, street, number, x, y, false);
    for (auto p : this->packages) {
        if (package == p) {
            throw runtime_error("Duplicate package data!");
        }
    }

    this->packages.push_back(package);
    this->savePackages();
    this->notify();
}

void Session::deliverPackage(Package &package) {
    for (auto &p : this->packages) {
        if (p == package) {
            p.setStatus(true);
            break;
        }
    }

    this->savePackages();
    this->notify();
}

Courier &Session::getCourierByIndex(int index) {
    return this->couriers[index];
}

vector<Courier> &Session::getCouriers() {
    return this->couriers;
}

vector<Package> &Session::getPackages() {
    return this->packages;
}

vector<Package> Session::getPackagesUndelivered() {
    vector<Package> undelivered;
    for (auto &package : this->packages) {
        if (!package.getStatus()) {
            undelivered.push_back(package);
        }
    }

    return undelivered;
}

vector<Package> Session::getAssignedPackages(Courier &courier) {
    vector<Package> assigned;
    for (auto &package : this->packages) {
        bool ok = false;
        for (auto street : courier.getStreets()) {
            if (package.getStreet() == street) {
                ok = true;
                break;
            }
        }

        if (courier.isInside(package.getX(), package.getY())) {
            ok = true;
        }

        if (ok) {
            assigned.push_back(package);
        }
    }

    return assigned;
}

