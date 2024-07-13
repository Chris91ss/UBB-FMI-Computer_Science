#include <QApplication>
#include <QPushButton>
#include <QSortFilterProxyModel>
#include "header_files/researchgui.h"
#include "header_files/IdeaModel.h"

using namespace std;

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    string researchersFile = "../resource_files/researchers.txt";
    string ideasFile = "../resource_files/ideas.txt";
    Repository repository{researchersFile, ideasFile};

    auto model = new IdeaModel{repository};

    auto guis = new ResearchGui[repository.getResearchers().size()];
    for (int i = 0; i < repository.getResearchers().size(); ++i) {
        guis[i].init(&repository.getResearcherByIndex(i), model);
        guis[i].show();
    }

    return QApplication::exec();
}
