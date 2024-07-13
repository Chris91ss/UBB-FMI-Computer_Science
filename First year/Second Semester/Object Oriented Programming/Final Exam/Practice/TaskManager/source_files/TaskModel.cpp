//
// Created by qdeni on 6/25/2023.
//

#include "../header_files/TaskModel.h"

int TaskModel::rowCount(const QModelIndex &parent) const {
    return int(this->taskRepository.getTasks().size());
}

int TaskModel::columnCount(const QModelIndex &parent) const {
    return 3;
}

QVariant TaskModel::data(const QModelIndex &index, int role) const {
    int row = index.row();

    if (role == Qt::DisplayRole) {
        Task task = this->taskRepository.getTasks()[row];

        switch (index.column()) {
            case 0:
                return QString::fromStdString(task.getDescription());
            case 1:
                return QString::fromStdString(task.getStatus());
            case 2: {
                Programmer programmer = this->taskRepository.getProgrammerById(task.getProgrammerId());
                return QString::fromStdString(programmer.getName());
            }
            default:
                break;
        }
    }

    return QVariant();
}

QVariant TaskModel::headerData(int section, Qt::Orientation orientation, int role) const {
    if (role == Qt::DisplayRole) {
        if (orientation == Qt::Horizontal) {
            switch (section) {
                case 0:
                    return QString("Description");
                case 1:
                    return QString("Status");
                case 2:
                    return QString("Programmer");
                default:
                    break;
            }
        }
    }

    return QVariant();
}

bool TaskModel::setData(const QModelIndex &index, const QVariant &value, int role) {
    return false;
}

Qt::ItemFlags TaskModel::flags(const QModelIndex &index) const {
    return Qt::ItemFlags{};
}
