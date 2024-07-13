//
// Created by qdeni on 6/25/2023.
//

#ifndef VOLUNTEERING_SUBJECT_H
#define VOLUNTEERING_SUBJECT_H

#include <vector>
#include "Observer.h"


class Subject {
private:
    std::vector<Observer *> observers;

public:
    void registerObserver(Observer *observer);

    void unregisterObserver(Observer *observer);

    void notify();
};


#endif //VOLUNTEERING_SUBJECT_H
