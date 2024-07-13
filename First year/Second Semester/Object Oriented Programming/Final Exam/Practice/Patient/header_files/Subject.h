//
// Created by qdeni on 6/26/2023.
//

#ifndef PATIENT_SUBJECT_H
#define PATIENT_SUBJECT_H

#include <vector>
#include "Observer.h"

class Subject {
private:
    std::vector<Observer*> observers;

public:
    void registerObserver(Observer *observer) {
        this->observers.push_back(observer);
    }

    void unregisterObserver(Observer *observer) {
        for (int i = 0; i < this->observers.size(); i++) {
            if (this->observers[i] == observer) {
                this->observers.erase(this->observers.begin() + i);
                return;
            }
        }
    }

    void notify() {
        for (auto &observer : this->observers) {
            observer->update();
        }
    }

};


#endif //PATIENT_SUBJECT_H
