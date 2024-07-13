#pragma once
#include <vector>
#include <iostream>
using namespace std;
#include "../repository/repository.h"
#include "../subject.h"

class Service : public Subject{
private:
    Repository *repo;
public:
    Service(Repository *repo);
    vector<Question*> getQuestions();
    vector<Participant*> getParticipants();
    void addQuestion(Question* q);
    void addParticipant(Participant* p);
    void removeQuestion(int id);
    void removeParticipant(string name);
    void updateParticipant(Participant* p, int score);
    void updateQuestion(Question* q, string text, string correctAnswer, int score);
    vector<Question*> getSortedById();
    vector<Question*> getSortedByScore();
    ~Service() = default;
};