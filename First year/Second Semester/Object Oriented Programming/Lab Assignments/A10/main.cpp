#include <QApplication>
#include <QPushButton>
#include "gui.h"
#include "headers/repository/textRepository.h"
#include "headers/service/service.h"

int main(int argc, char* argv[])
{
    QApplication a(argc, argv);
    TextRepository textRepository("../data/data.txt");
    textRepository.readFromFile();
    Service service(textRepository);
    GUI gui(nullptr, service);
    gui.show();
    return QApplication::exec();
}
