//
// Created by qdeni on 6/25/2023.
//

#include "../header_files/Subject.h"

void Subject::registerObserver(Observer *observer) {
    this->observers.push_back(observer);
}

void Subject::unregisterObserver(Observer *observer) {
    for (auto it = observers.begin(); it != observers.end(); it++) {
        if (*it == observer) {
            observers.erase(it);
            break;
        }
    }
}

void Subject::notify() {
    for (auto &observer : observers) {
        observer->update();
    }
}
