#include "question.h"


Question::Question(int id, string text, string correctAnswer, int score) {
    this->id = id;
    this->text = text;
    this->correctAnswer = correctAnswer;
    this->score = score;
}

int Question::getId() {
    return this->id;
}

string Question::getText() {
    return this->text;
}

string Question::getCorrectAnswer() {
    return this->correctAnswer;
}

int Question::getScore() {
    return this->score;
}

void Question::setId(int id) {
    this->id = id;
}

void Question::setText(string text) {
    this->text = text;
}

void Question::setCorrectAnswer(string correctAnswer) {
    this->correctAnswer = correctAnswer;
}

void Question::setScore(int score) {
    this->score = score;
}

ostream &operator<<(ostream &os, const Question &q) {
    os << q.id << ";" << q.text << ";" << q.correctAnswer << ";" << q.score;
    return os;
}

istream &operator>>(istream &is, Question &q) {
    is >> q.id >> q.text >> q.correctAnswer >> q.score;
    return is;
}

string Question::toString() {
    return to_string(this->id) + ";" + this->text + ";" + this->correctAnswer + ";" + to_string(this->score);
}

string Question::toStringParticipant() {
    return to_string(this->id) + ";" + this->text + ";" + to_string(this->score);
}
