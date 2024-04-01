#include "ui/ui.h"

int main()
{
    Repository<School> repository;
    Service service(repository);
    UI ui(service);
    ui.run();
    return 0;
}