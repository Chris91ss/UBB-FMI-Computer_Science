//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_RESEARCHGUI_H
#define RESEARCH_RESEARCHGUI_H

#include <QWidget>
#include <QAbstractItemModel>
#include "Controller.h"
#include "IdeaModel.h"


QT_BEGIN_NAMESPACE
namespace Ui { class ResearchGui; }
QT_END_NAMESPACE

class ResearchGui : public QWidget {
Q_OBJECT

private:
    Researcher *researcher;
    IdeaModel *ideaModel;

public:
    explicit ResearchGui(QWidget *parent = nullptr);

    ~ResearchGui() override;

    void init(Researcher *researcher, IdeaModel *ideaModel);

private:
    void makeConnections();

    void addIdea();

    void updateIdea();

private:

    Ui::ResearchGui *ui;
};


#endif //RESEARCH_RESEARCHGUI_H
