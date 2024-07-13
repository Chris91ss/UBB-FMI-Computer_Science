#pragma once
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

class Participant{
private:
    string name;
    int score;
public:
    Participant(string name, int score);
    string getName();
    int getScore();
    void setName(string name);
    void setScore(int score);
    friend ostream& operator<<(ostream& os, const Participant& p);
    friend istream& operator>>(istream& is, Participant& p);
    string toString();
};