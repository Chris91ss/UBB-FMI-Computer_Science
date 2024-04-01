#include "service/service.h"

class UI {
private:
    Service service;
public:
    UI(const Service &service);
    ~UI();
    void run();

private:
    static void printMenu();
    void addSchoolUI();
    void removeSchoolUI();
    void GetAllSchoolsUI();
    void GetAllSchoolsSortedUI();
    void GetAllSchoolsAfterAGivenDateUI();
};