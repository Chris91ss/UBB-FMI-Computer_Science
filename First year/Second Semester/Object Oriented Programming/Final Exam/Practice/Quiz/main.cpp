#include <QApplication>
#include <QPushButton>
#include "repository/repository.h"
#include "service/service.h"
#include "gui.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Repository repo;
    Service service(&repo);
    for(auto &participant : service.getParticipants())
    {
        auto g = new gui(nullptr, &service, participant);
        g->show();
    }

    auto g = new gui(nullptr, &service, nullptr);
    g->show();
    return QApplication::exec();
}
