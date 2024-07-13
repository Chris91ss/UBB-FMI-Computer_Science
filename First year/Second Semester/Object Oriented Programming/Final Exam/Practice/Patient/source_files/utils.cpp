//
// Created by qdeni on 6/26/2023.
//

#include "../header_files/utils.h"

std::string trim(const std::string &str) {
    std::string result = str;

    while (result[0] == ' ') {
        result.erase(0, 1);
    }
    while (result[result.size() - 1] == ' ') {
        result.erase(result.size() - 1, 1);
    }

    return result;
}

std::vector<std::string> tokenize(const std::string &str, char delim) {
    std::vector<std::string> result;
    std::stringstream ss(str);

    std::string token;
    while (getline(ss, token, delim)) {
        result.push_back(trim(token));
    }

    return result;
}
