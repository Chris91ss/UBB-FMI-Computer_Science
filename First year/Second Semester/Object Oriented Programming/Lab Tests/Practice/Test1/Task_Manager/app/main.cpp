#include "ui/ui.h"

int main()
{
    Repository<Task> repository;
    Service service(repository);
    UI ui(service);
    ui.Run();
    return 0;
}