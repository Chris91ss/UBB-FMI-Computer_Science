//
// Created by qdeni on 6/26/2023.
//

#include "../header_files/IdeaModel.h"

using namespace std;

int IdeaModel::rowCount(const QModelIndex &parent) const {
    return int(this->repository.getIdeas().size()) + 1;
}

int IdeaModel::columnCount(const QModelIndex &parent) const {
    return 4;
}

QVariant IdeaModel::data(const QModelIndex &index, int role) const {
    int row = index.row();
    int column = index.column();
    if (row == int(this->repository.getIdeas().size())) {
        return QVariant();
    }

    if (role == Qt::DisplayRole) {

        Idea idea = this->repository.getIdeas()[row];
        switch (column) {
            case 0:
                return QString::fromStdString(idea.getTitle());
            case 1:
                return QString::fromStdString(idea.getStatus());
            case 2:
                return QString::fromStdString(idea.getCreator());
            case 3:
                return QString::fromStdString(to_string(idea.getDuration()));
            default:
                break;
        }
    }

    return QVariant();
}

QVariant IdeaModel::headerData(int section, Qt::Orientation orientation, int role) const {
    if (role == Qt::DisplayRole) {
        if (orientation == Qt::Horizontal) {
            switch (section) {
                case 0:
                    return QString("Title");
                case 1:
                    return QString("Status");
                case 2:
                    return QString("Creator");
                case 3:
                    return QString("Duration");
                default:
                    break;
            }
        }
    }

    return QVariant();
}

bool IdeaModel::setData(const QModelIndex &index, const QVariant &value, int role) {
    return false;
}

Qt::ItemFlags IdeaModel::flags(const QModelIndex &index) const {
    return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsEditable;
}

void IdeaModel::addIdea(const std::string &title) {
    if (title.empty()) {
        throw runtime_error("Invalid idea data!");
    }

    Idea idea(title, "description", "proposed", "none", 0);
    for (auto &i : this->repository.getIdeas()) {
        if (i.getTitle() == title) {
            throw runtime_error("Idea already exists!");
        }
    }
    this->repository.addIdea(idea);

    int lastRow = rowCount();
    beginInsertRows(QModelIndex(), lastRow, lastRow);
    endInsertRows();

    emit layoutChanged();
}
