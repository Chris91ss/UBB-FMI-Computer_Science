//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_SUBJECT_H
#define DRIVE_SUBJECT_H

#include <vector>
#include "Observer.h"

class Subject {
private:
    std::vector<Observer *> observers;

public:
    void registerObserver(Observer *observer) {
        this->observers.push_back(observer);
    }

    void unregisterObserver(Observer *observer) {
        for (auto it = this->observers.begin(); it != this->observers.end(); ++it) {
            if (*it == observer) {
                this->observers.erase(it);
                break;
            }
        }
    }

    void notify() {
        for (auto observer : this->observers) {
            observer->update();
        }
    }
};


#endif //DRIVE_SUBJECT_H
