#include "../headers/ui/ui.h"
#include "../tests/testAllFunctions.h"

int main() {
    Repository *repository = CreateRepository();
    Stack *undoStack = CreateStack(2, (DestroyFunction) DestroyRepository);
    Stack *redoStack = CreateStack(2, (DestroyFunction) DestroyRepository);

    Service *service = CreateService(repository, undoStack, redoStack);
    UI *ui = CreateUI(service);

    TestAllFunctions();
    RunApp(ui);
    DestroyUI(ui);
    return 0;
}

