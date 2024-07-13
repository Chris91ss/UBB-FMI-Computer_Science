#include "service.h"

Service::Service(Repository *repo) {
    this->repo = repo;
    this->repo->loadQuestions("../data/questions.txt");
    this->repo->loadParticipants("../data/participants.txt");
}

vector<Question*> Service::getQuestions() {
    return this->repo->getQuestions();
}

vector<Participant*> Service::getParticipants() {
    return this->repo->getParticipants();
}

void Service::addQuestion(Question* q) {
    for(auto & question : this->repo->getQuestions())
    {
        if(question->getId() == q->getId())
        {
            throw runtime_error("Question already exists!");
        }
    }
    this->repo->addQuestion(q);
    notify();
}

void Service::addParticipant(Participant* p) {
    this->repo->addParticipant(p);
    notify();
}

void Service::removeQuestion(int id) {
    this->repo->removeQuestion(id);
    notify();
}

void Service::removeParticipant(string name) {
    this->repo->removeParticipant(name);
    notify();
}

void Service::updateParticipant(Participant* p, int score) {
    this->repo->updateParticipant(p, score);
    notify();
}

void Service::updateQuestion(Question* q, string text, string correctAnswer, int score) {
    this->repo->updateQuestion(q, text, correctAnswer, score);
    notify();
}

vector<Question*> Service::getSortedById() {
    vector<Question*> questions = this->repo->getQuestions();
    sort(questions.begin(), questions.end(), [](Question* q1, Question* q2) {
        return q1->getId() < q2->getId();
    });
    return questions;
}

vector<Question*> Service::getSortedByScore() {
    vector<Question*> questions = this->repo->getQuestions();
    sort(questions.begin(), questions.end(), [](Question* q1, Question* q2) {
        return q1->getScore() < q2->getScore();
    });
    return questions;
}



