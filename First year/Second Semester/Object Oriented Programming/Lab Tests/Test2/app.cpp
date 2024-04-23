#include "ui/ui.h"

int main()
{
    Repository repo;

    repo.addAppliance(new Refrigerator("1", "A", true));
    repo.addAppliance(new Refrigerator("2", "A++", false));
    repo.addAppliance(new DishWasher("3", 2));
    repo.addAppliance(new DishWasher("4", 10));

    UI ui(repo);
    ui.run();
    return 0;
}