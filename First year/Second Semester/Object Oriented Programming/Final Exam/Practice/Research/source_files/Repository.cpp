//
// Created by qdeni on 6/26/2023.
//

#include "../header_files/Repository.h"

using namespace std;

Repository::Repository(const string &researchersFile, const string &ideasFile) : researchersFile(researchersFile),
                                                                                 ideasFile(ideasFile) {
    this->loadResearchers();
    this->loadIdeas();
}

void Repository::loadResearchers() {
    ifstream file(this->researchersFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open file " + this->researchersFile);
    }

    Researcher researcher;
    while(file >> researcher) {
        this->researchers.push_back(researcher);
    }

    file.close();
}

void Repository::loadIdeas() {
    ifstream file(this->ideasFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open file " + this->ideasFile);
    }

    Idea idea;
    while(file >> idea) {
        this->ideas.push_back(idea);
    }

    file.close();
}

void Repository::saveIdeas() {
    ofstream file(this->ideasFile);
    if (!file.is_open()) {
        throw runtime_error("Could not open file " + this->ideasFile);
    }

    for (const auto &idea : this->ideas) {
        file << idea << endl;
    }

    file.close();
}

void Repository::addIdea(const Idea &idea) {
    this->ideas.push_back(idea);
    this->saveIdeas();
}

Researcher &Repository::getResearcherByIndex(int index) {
    return this->researchers[index];
}

vector<Researcher> &Repository::getResearchers() {
    return this->researchers;
}

vector<Idea> &Repository::getIdeas() {
    return this->ideas;
}
