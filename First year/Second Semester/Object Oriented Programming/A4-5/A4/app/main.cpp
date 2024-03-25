#include "../headers/ui/ui.h"
#include "../tests/test.h"

int main()
{
    Repository<TrenchCoat> repository;
    Service service(repository);
    UI ui(service);

    ui.Run();

    Test::TestAll();

    return 0;
}