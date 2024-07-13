#include <QApplication>
#include <QPushButton>
#include "gui.h"
#include "repository/repository.h"
#include "service/service.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Repository repo;
    Service service(&repo);
    for(auto * person : service.getPersons()){
        auto g = new gui(nullptr, &service, person);
        g->show();
    }
    return QApplication::exec();
}
