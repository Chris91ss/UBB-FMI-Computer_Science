//
// Created by qdeni on 6/28/2023.
//

#ifndef E916_DENIS916_SUBJECT_H
#define E916_DENIS916_SUBJECT_H

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
        for (auto it = this->observers.begin(); it != this->observers.end(); it++) {
            if (*it == observer) {
                this->observers.erase(it);
            }
        }
    }

    void notify() {
        for (auto observer : this->observers) {
            observer->update();
        }
    }
};


#endif //E916_DENIS916_SUBJECT_H
