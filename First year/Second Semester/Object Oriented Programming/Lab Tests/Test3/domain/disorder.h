#pragma once
#include <string>
#include <vector>
using namespace std;

class Disorder {
private:
    string category;
    string name;
    vector<string> symptoms;
public:
    Disorder(string category, string name, vector<string> symptoms);
    string toString() const;
    string getName();
    string getCategory();
    vector<string> getSymptoms() const;

};