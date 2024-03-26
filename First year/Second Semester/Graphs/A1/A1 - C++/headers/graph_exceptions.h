#pragma once
#include <stdexcept>

using namespace std;

class GraphException : public exception {
private:
    string message;
public:
    GraphException(const string& msg) : message(msg) {}

    // Override what() method to provide custom error message
    const char* what() const noexcept override
    {
        return message.c_str();
    }
};
