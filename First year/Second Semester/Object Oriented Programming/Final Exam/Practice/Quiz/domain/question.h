#pragma once
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

class Question{
private:
    int id;
    string text;
    string correctAnswer;
    int score;
public:
    Question(int id, string text, string correctAnswer, int score);
    int getId();
    string getText();
    string getCorrectAnswer();
    int getScore();
    void setId(int id);
    void setText(string text);
    void setCorrectAnswer(string correctAnswer);
    void setScore(int score);
    friend ostream& operator<<(ostream& os, const Question& q);
    friend istream& operator>>(istream& is, Question& q);
    string toString();
    string toStringParticipant();
};