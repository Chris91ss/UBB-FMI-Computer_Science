#pragma once

#include "observer.h"
#include <vector>
#include <algorithm>
using namespace std;

class Subject {
private:
    vector<Observer*> observers;
public:
    void registerObserver(Observer* observer)
    {
        this->observers.push_back(observer);
    }
    void unregisteredObserver(Observer* observer)
    {
        this->observers.erase(remove(this->observers.begin(), this->observers.end(), observer), this->observers.end());
    }

    void notify()
    {
        for (auto observer : this->observers)
        {
            observer->update();
        }
    }
};