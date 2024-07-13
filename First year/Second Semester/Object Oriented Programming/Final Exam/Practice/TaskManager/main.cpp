#include <QApplication>
#include <QSortFilterProxyModel>
#include "header_files/TaskRepository.h"
#include "header_files/taskmanager.h"
#include "header_files/TaskModel.h"
#include "header_files/Controller.h"

using namespace std;


int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string programmersFile = "../resource_files/programmers.txt";
    string tasksFile = "../resource_files/tasks.txt";

    TaskRepository repo{programmersFile, tasksFile};
    Controller controller{repo};

    auto *model = new TaskModel{repo};

    auto *sortModel = new QSortFilterProxyModel{};
    sortModel->setSourceModel(model);
    sortModel->sort(1, Qt::AscendingOrder);

    auto managers = new TaskManager[repo.getProgrammers().size()];
    for (int i = 0; i < repo.getProgrammers().size(); ++i) {
        managers[i].init(sortModel, &controller, &controller.getProgrammerByIndex(i));
        managers[i].show();
    }

    return QApplication::exec();
}
