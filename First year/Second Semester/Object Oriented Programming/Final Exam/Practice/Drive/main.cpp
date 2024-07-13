#include <QApplication>
#include "header_files/drivergui.h"
#include "header_files/map.h"

using namespace std;

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string driversFile = "../resource_files/drivers.txt";
    string reportsFile = "../resource_files/reports.txt";
    Controller controller(driversFile, reportsFile);

    auto guis = new DriverGui[controller.getDrivers().size()];
    for (int i = 0; i < controller.getDrivers().size(); ++i) {
        guis[i].init(&controller.getDriverByIndex(i), &controller);
    }

    Map map(controller);
    map.show();

    return QApplication::exec();
}
