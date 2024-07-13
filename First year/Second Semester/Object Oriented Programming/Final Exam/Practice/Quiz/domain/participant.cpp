#include "participant.h"

Participant::Participant(string name, int score) {
    this->name = name;
    this->score = score;
}

string Participant::getName() {
    return this->name;
}

int Participant::getScore() {
    return this->score;
}

void Participant::setName(string name) {
    this->name = name;
}

void Participant::setScore(int score) {
    this->score = score;
}

ostream &operator<<(ostream &os, const Participant &p) {
    os << p.name << ";" << p.score;
    return os;
}

istream &operator>>(istream &is, Participant &p) {
    is >> p.name >> p.score;
    return is;
}

string Participant::toString() {
    return this->name + ";" + to_string(this->score);
}

