//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_REPOSITORY_H
#define RESEARCH_REPOSITORY_H

#include "Researcher.h"
#include "Idea.h"

class Repository {
private:
    std::string researchersFile;
    std::string ideasFile;
    std::vector<Researcher> researchers;
    std::vector<Idea> ideas;

public:
    Repository(const std::string &researchersFile, const std::string &ideasFile);

    void addIdea(const Idea &idea);

    Researcher &getResearcherByIndex(int index);

    std::vector<Researcher> &getResearchers();

    std::vector<Idea> &getIdeas();

private:
    void loadResearchers();

    void loadIdeas();

    void saveIdeas();
};


#endif //RESEARCH_REPOSITORY_H
