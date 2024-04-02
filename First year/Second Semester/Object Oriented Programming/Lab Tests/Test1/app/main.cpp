#include "ui/ui.h"
#include "../tests/testAll.h"

int main()
{
    Repository<Bill> repository;
    Service service(repository);
    UI ui(service);
    ui.run();
    return 0;
}