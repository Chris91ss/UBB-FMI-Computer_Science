//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_IDEAMODEL_H
#define RESEARCH_IDEAMODEL_H

#include <QAbstractTableModel>
#include "Repository.h"


class IdeaModel : public QAbstractTableModel {
private:
    Repository &repository;

public:
    IdeaModel(Repository &repository) : repository(repository) {}

    int rowCount(const QModelIndex &parent = QModelIndex()) const;

    int columnCount(const QModelIndex &parent = QModelIndex()) const;

    QVariant data(const QModelIndex &index, int role) const override;

    QVariant headerData(int section, Qt::Orientation orientation, int role) const override;

    bool setData(const QModelIndex &index, const QVariant &value, int role) override;

    Qt::ItemFlags flags(const QModelIndex &index) const override;

public:
    void addIdea(const std::string &title);

    Idea &getIdeaByIndex(int index) {
        return this->repository.getIdeas()[index];
    }
};


#endif //RESEARCH_IDEAMODEL_H
