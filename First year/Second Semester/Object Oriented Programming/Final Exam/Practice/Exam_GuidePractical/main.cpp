#include <QApplication>
#include <QPushButton>
#include "gui.h"
#include "repository/repository.h"
#include "service/service.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Repository repo;
    Service service(&repo);
    for(User *user: service.getUsersFromRepo()) {
        auto gui = new GUI(nullptr, &service, user);
        gui->show();
    }

    return QApplication::exec();
}
