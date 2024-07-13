#include <QApplication>
#include "header_files/doctorgui.h"
#include "header_files/statisticgui.h"

using namespace std;

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string doctorsFile = "../resource_files/doctors.txt";
    string patientsFile = "../resource_files/patients.txt";

    Controller controller(doctorsFile, patientsFile);

    auto guis = new DoctorGui[controller.getDoctors().size()];
    for (int i = 0; i < controller.getDoctors().size(); ++i) {
        guis[i].init(&controller, controller.getDoctorByIndex(i));
    }

    StatisticGui statisticGui(controller);

    return QApplication::exec();
}
