#pragma once
#include <string>
#include <vector>
#include <fstream>
#include <stdexcept>
#include "../domain/medicalAnalysis.h"

using namespace std;

class Person {
private:
    vector<MedicalAnalysis*> analyses;
    string name;
public:
    explicit Person(string name);
    void addAnalysis(MedicalAnalysis* analysis);
    vector<MedicalAnalysis*> getAllAnalyses() const;
    vector<MedicalAnalysis*> getAnalysesByMonth(int month) const;
    bool isIll(int month) const;
    vector<MedicalAnalysis*> getAnalysesBetweenDates(const string &date1, const string &date2) const;
    void writeToFile(const string &filename, const string &date1, const string &date2) const;
    ~Person();
};