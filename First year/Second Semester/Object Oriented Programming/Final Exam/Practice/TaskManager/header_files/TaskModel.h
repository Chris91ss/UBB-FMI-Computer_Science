//
// Created by qdeni on 6/25/2023.
//

#ifndef TASKMANAGER_TASKMODEL_H
#define TASKMANAGER_TASKMODEL_H

#include <QAbstractTableModel>
#include "TaskRepository.h"

class TaskModel : public QAbstractTableModel {

private:
    TaskRepository &taskRepository;

public:
    TaskModel(TaskRepository &taskRepository) : taskRepository(taskRepository) {};

    int rowCount(const QModelIndex &parent = QModelIndex()) const;

    int columnCount(const QModelIndex &parent = QModelIndex()) const;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;

    QVariant headerData(int section, Qt::Orientation orientation, int role) const override;

    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole);

    Qt::ItemFlags flags(const QModelIndex &index) const override;

};


#endif //TASKMANAGER_TASKMODEL_H
