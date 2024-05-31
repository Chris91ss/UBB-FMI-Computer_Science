#include <QApplication>
#include <QPushButton>

#include "gui.h"
#include "repository/repository.h"
#include "service/service.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Repository repository;
    Service service(&repository);
    service.readFromFile("../bills.txt");
    GUI gui(nullptr, service);
    gui.show();
    return QApplication::exec();
}
