
#include "person.h"

#include <utility>

Person::Person(string name) {
    this->name = std::move(name);
}

void Person::addAnalysis(MedicalAnalysis* analysis) {
    analyses.push_back(analysis);
}

vector<MedicalAnalysis*> Person::getAllAnalyses() const {
    return analyses;
}

vector<MedicalAnalysis*> Person::getAnalysesByMonth(int month) const {
    vector<MedicalAnalysis*> monthlyAnalyses;
    for (auto* analysis : analyses) {
        int analysisMonth = stoi(analysis->date.substr(5, 2));
        if (analysisMonth == month) {
            monthlyAnalyses.push_back(analysis);
        }
    }
    return monthlyAnalyses;
}

bool Person::isIll(int month) const {
    vector<MedicalAnalysis*> monthlyAnalyses = getAnalysesByMonth(month);
    for (auto* analysis : monthlyAnalyses) {
        if (analysis->isResultOK()) {
            return false;
        }
    }
    return true;
}

vector<MedicalAnalysis*> Person::getAnalysesBetweenDates(const string &date1, const string &date2) const {
    vector<MedicalAnalysis*> filteredAnalyses;
    for (auto* analysis : analyses) {
        if (analysis->date >= date1 && analysis->date <= date2) {
            filteredAnalyses.push_back(analysis);
        }
    }
    return filteredAnalyses;
}

void Person::writeToFile(const string &filename, const string &date1, const string &date2) const {
    ofstream file(filename);
    if (!file) {
        throw runtime_error("Could not open file " + filename);
    }
    for (auto* analysis : getAnalysesBetweenDates(date1, date2)) {
        file << analysis->toString() << '\n';
    }
    file.close();
}

Person::~Person() {
    for (auto analysis : analyses) {
        delete analysis;
    }
}
