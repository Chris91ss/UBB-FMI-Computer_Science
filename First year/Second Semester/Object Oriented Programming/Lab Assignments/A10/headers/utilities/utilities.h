#pragma once

#include <string>
#include <vector>
#include <sstream>

using namespace std;

/// Tokenizes a string. It splits the string into a vector of strings using the delimiter.
///
/// \param str - the string to be tokenized
/// \param delimiter - the delimiter
/// \return - vector <string> - the vector of strings
vector<std::string> tokenize(const std::string &str, char delimiter);