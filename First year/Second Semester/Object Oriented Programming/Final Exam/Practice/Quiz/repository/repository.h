#pragma once
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "../domain/participant.h"
#include "../domain/question.h"
using namespace std;

class Repository{
private:
    vector<Question*> questions;
    vector<Participant*> participants;
public:
    Repository() = default;
    vector<Question*> getQuestions();
    vector<Participant*> getParticipants();
    void addQuestion(Question* q);
    void addParticipant(Participant* p);
    void removeQuestion(int id);
    void removeParticipant(string name);
    void updateParticipant(Participant* p, int score);
    void updateQuestion(Question* q, string text, string correctAnswer, int score);
    void loadQuestions(string filename);
    void loadParticipants(string filename);
    void saveQuestions(string filename);
    void saveParticipants(string filename);
    ~Repository() = default;
};