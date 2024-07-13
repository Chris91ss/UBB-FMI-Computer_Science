#include <QApplication>
#include "header_files/departmentgui.h"
#include "header_files/departmentsoverview.h"

using namespace std;

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string departmentsFile = "../resource_files/departments.txt";
    string volunteersFile = "../resource_files/volunteers.txt";
    Repository repo{departmentsFile, volunteersFile};
    Controller controller{repo};

    auto departments = controller.getDepartments();
    auto guis = new DepartmentGui[departments.size()];
    for (int i = 0; i < departments.size(); i++) {
        guis[i].init(&controller, controller.getDepartment(i));
        guis[i].show();
    }

    DepartmentsOverview overview{controller};
    overview.show();

    return QApplication::exec();
}
