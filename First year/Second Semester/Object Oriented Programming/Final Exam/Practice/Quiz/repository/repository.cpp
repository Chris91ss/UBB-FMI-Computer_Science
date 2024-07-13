#include "repository.h"

vector<Question*> Repository::getQuestions() {
    return this->questions;
}

vector<Participant*> Repository::getParticipants() {
    return this->participants;
}

void Repository::addQuestion(Question* q) {
    this->questions.push_back(q);
    saveQuestions("../data/questions.txt");
}

void Repository::addParticipant(Participant* p) {
    this->participants.push_back(p);
    saveParticipants("../data/participants.txt");
}

void Repository::removeQuestion(int id) {
    for (int i = 0; i < this->questions.size(); i++) {
        if (this->questions[i]->getId() == id) {
            this->questions.erase(this->questions.begin() + i);
            saveQuestions("../data/questions.txt");
            return;
        }
    }
}

void Repository::removeParticipant(string name) {
    for (int i = 0; i < this->participants.size(); i++) {
        if (this->participants[i]->getName() == name) {
            this->participants.erase(this->participants.begin() + i);
            saveParticipants("../data/participants.txt");
            return;
        }
    }
}

void Repository::updateParticipant(Participant* p, int score) {
    for (int i = 0; i < this->participants.size(); i++) {
        if (this->participants[i]->getName() == p->getName()) {
            this->participants[i]->setScore(score);
            saveParticipants("../data/participants.txt");
            return;
        }
    }
}

void Repository::updateQuestion(Question* q, string text, string correctAnswer, int score) {
    for (int i = 0; i < this->questions.size(); i++) {
        if (this->questions[i]->getId() == q->getId()) {
            this->questions[i]->setText(text);
            this->questions[i]->setCorrectAnswer(correctAnswer);
            this->questions[i]->setScore(score);
            saveQuestions("../data/questions.txt");
            return;
        }
    }
}

void Repository::loadQuestions(string filename) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string id_str, score_str, text, correctAnswer;

        getline(ss, id_str, ';');
        getline(ss, text, ';');
        getline(ss, correctAnswer, ';');
        getline(ss, score_str, ';');

        int id = stoi(id_str);
        int score = stoi(score_str);

        this->questions.push_back(new Question(id, text, correctAnswer, score));
    }
    file.close();
}

void Repository::loadParticipants(string filename) {
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string name, score_str;

        getline(ss, name, ';');
        getline(ss, score_str, ';');

        int score = stoi(score_str);

        this->participants.push_back(new Participant(name, score));
    }
    file.close();
}

void Repository::saveQuestions(string filename) {
    ofstream file(filename);
    for (auto q : this->questions) {
        file << q->getId() << ";" << q->getText() << ";" << q->getCorrectAnswer() << ";" << q->getScore() << endl;
    }
    file.close();
}

void Repository::saveParticipants(string filename) {
    ofstream file(filename);
    for (auto p : this->participants) {
        file << p->getName() << ";" << p->getScore() << endl;
    }
    file.close();
}




