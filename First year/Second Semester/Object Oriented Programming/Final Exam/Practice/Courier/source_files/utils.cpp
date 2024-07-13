//
// Created by qdeni on 6/28/2023.
//

#include "../header_files/utils.h"

using namespace std;

string trim(const string &str) {
    string result = str;

    while (result[0] == ' ') {
        result.erase(0, 1);
    }
    while (result[result.size() - 1] == ' ') {
        result.erase(result.size() - 1, 1);
    }

    return result;
}

vector<string> tokenize(const string &str, char delim) {
    vector<string> result;
    stringstream ss(str);

    string aux;
    while (getline(ss, aux, delim)) {
        result.push_back(trim(aux));
    }

    return result;
}
