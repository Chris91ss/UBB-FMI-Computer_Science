#include <QApplication>
#include <QPushButton>

#include "gui.h"

int main(int argc, char* argv[])
{
    QApplication a(argc, argv);
    Repository repository;
    Service service(&repository);
    service.readFromFile("../disorders.txt");
    GUI gui(nullptr, service);
    gui.show();
    return QApplication::exec();
}
