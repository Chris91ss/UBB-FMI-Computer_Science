//
// Created by qdeni on 6/26/2023.
//

// You may need to build the project (run Qt uic code generator) to get "ui_ResearchGui.h" resolved

#include "../header_files/researchgui.h"
#include "../form_files/ui_ResearchGui.h"

using namespace std;

ResearchGui::ResearchGui(QWidget *parent) :
        QWidget(parent), ui(new Ui::ResearchGui), researcher(nullptr),
        ideaModel(nullptr) {
    this->ui->setupUi(this);
}

ResearchGui::~ResearchGui() {
    delete this->ui;
}

void ResearchGui::makeConnections() {
    QWidget::connect(this->ui->AddButton, &QPushButton::clicked, this, &ResearchGui::addIdea);
    QWidget::connect(this->ui->updateButton, &QPushButton::clicked, this, &ResearchGui::updateIdea);
}

void ResearchGui::init(Researcher *researcher, IdeaModel *ideaModel) {
    this->researcher = researcher;
    this->ideaModel = ideaModel;

    this->ui->ideasTableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    this->ui->ideasTableView->setModel(this->ideaModel);
    this->setWindowTitle(QString::fromStdString(this->researcher->getName()));
    this->makeConnections();
}

void ResearchGui::addIdea() {
    this->ideaModel->addIdea("New idea");
}

void ResearchGui::updateIdea() {
    QModelIndexList selectedIndexes = this->ui->ideasTableView->selectionModel()->selectedIndexes();
    if (selectedIndexes.empty()) {
        return;
    }

    int row = selectedIndexes.at(0).row();
    Idea &idea = this->ideaModel->getIdeaByIndex(row);
    idea.setStatus("accepted");
    this->ideaModel->layoutChanged();
}
