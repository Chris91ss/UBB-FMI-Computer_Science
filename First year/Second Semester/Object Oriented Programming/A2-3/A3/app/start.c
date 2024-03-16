#include "../headers/ui/ui.h"

int main() {
    Repository *repository = CreateRepository();
    Service *service = CreateService(repository);
    UI *ui = CreateUI(service);
    RunApp(ui);
    DestroyUI(ui);
    return 0;
}

