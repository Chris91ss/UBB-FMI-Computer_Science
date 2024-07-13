//
// Created by qdeni on 6/26/2023.
//

#ifndef RESEARCH_CONTROLLER_H
#define RESEARCH_CONTROLLER_H

#include "Repository.h"


class Controller {
private:
    Repository &repository;

public:
    Controller(Repository &repository) : repository(repository) {}

    void addIdea(const std::string &title, const std::string &description, const std::string &creator, int duration);

    Researcher &getResearcherByIndex(int index);

    std::vector<Researcher> &getResearchers();
};


#endif //RESEARCH_CONTROLLER_H
