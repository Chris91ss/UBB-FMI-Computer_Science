#pragma once

#include <QAbstractTableModel>
#include "headers/domain/trenchCoat.h"
#include <vector>

class BasketModel : public QAbstractTableModel {

public:
    explicit BasketModel(const std::vector<TrenchCoat> &basket, QObject *parent = nullptr)
        : QAbstractTableModel(parent), basket(basket) {}

    int rowCount(const QModelIndex &parent = QModelIndex()) const override {
        return basket.size();
    }

    int columnCount(const QModelIndex &parent = QModelIndex()) const override {
        return 5; // Size, Color, Price, Quantity, Photo
    }

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override {
        if (!index.isValid() || role != Qt::DisplayRole) {
            return QVariant();
        }

        const TrenchCoat &coat = basket[index.row()];
        switch (index.column()) {
            case 0: return QString::fromStdString(coat.GetSize());
            case 1: return QString::fromStdString(coat.GetColor());
            case 2: return coat.GetPrice();
            case 3: return coat.GetQuantity();
            case 4: return QString::fromStdString(coat.GetPhotograph());
            default: return QVariant();
        }
    }

    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override {
        if (role != Qt::DisplayRole) {
            return QVariant();
        }

        if (orientation == Qt::Horizontal) {
            switch (section) {
                case 0: return QString("Size");
                case 1: return QString("Color");
                case 2: return QString("Price");
                case 3: return QString("Quantity");
                case 4: return QString("Photo");
                default: return QVariant();
            }
        }
        return QVariant();
    }

private:
    std::vector<TrenchCoat> basket;
};