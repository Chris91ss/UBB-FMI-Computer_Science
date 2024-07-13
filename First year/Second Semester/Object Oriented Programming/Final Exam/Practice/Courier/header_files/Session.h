//
// Created by qdeni on 6/28/2023.
//

#ifndef E916_DENIS916_SESSION_H
#define E916_DENIS916_SESSION_H

#include "Subject.h"
#include "Courier.h"
#include "Package.h"

class Session : public Subject {
private:
    std::vector<Courier> couriers;
    std::vector<Package> packages;
    std::string couriersFile;
    std::string packagesFile;

public:
    Session(const std::string &couriersFile, const std::string &packagesFile);

    void addPackage(const std::string &recipient, const std::string &street, int number, int x, int y);

    void deliverPackage(Package &package);

    Courier &getCourierByIndex(int index);

    std::vector<Courier> &getCouriers();

    std::vector<Package> &getPackages();

    std::vector<Package> getPackagesUndelivered();

    std::vector<Package> getAssignedPackages(Courier &courier);


private:
    void loadCouriers();

    void loadPackages();

    void savePackages();
};


#endif //E916_DENIS916_SESSION_H
