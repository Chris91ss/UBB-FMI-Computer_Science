#include "ui/ui.h"

int main()
{
    Repository<Bill> repository;
    Service service(repository);
    UI ui(service);
    ui.run();
    return 0;
}