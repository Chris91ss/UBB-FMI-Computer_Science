//
// Created by qdeni on 6/26/2023.
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

vector<string> tokenize(const string &str, char delimiter) {
    vector<string> result;
    stringstream ss(str);

    string token;
    while (getline(ss, token, delimiter)) {
        result.push_back(trim(token));
    }

    return result;
}
