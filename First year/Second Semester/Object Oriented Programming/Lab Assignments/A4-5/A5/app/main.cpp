#include "../headers/ui/ui.h"
#include "../tests/test.h"

int main()
{
    Repository<TrenchCoat> repository;
    Repository<TrenchCoat> shoppingBasket;
    Service service(repository);
    Service shoppingBasketService(shoppingBasket);
    UI ui(service, shoppingBasketService);

    ui.Run();

    Test::TestAll();

    return 0;
}