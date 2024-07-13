#pragma once
#include <string>
#include <vector>
#include <iostream>
using namespace std;

template<typename T>
class ToDo {
private:
    vector<T> items;
public:
    ToDo operator+=(T &item) {
        items.push_back(item);
        return *this;
    }

    typename vector<T>::iterator begin() {
        return items.begin();
    }

    typename vector<T>::iterator end() {
        return items.end();
    }

    void reversePrint(ostream &os) {
        for (auto it = items.rbegin(); it != items.rend(); ++it)
            os << *it << '\n';
    }
};

class Activity {
private:
    string description;
    string time;
public:
    Activity(string description, string time) : description(description), time(time) {}
    friend ostream& operator<<(ostream& os, const Activity &activity) {
        return os << "Activity " << activity.description << " will take place at " << activity.time << ".";
    }
};