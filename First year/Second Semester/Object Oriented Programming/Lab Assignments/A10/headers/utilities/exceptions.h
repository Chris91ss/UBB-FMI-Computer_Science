#pragma once
#include <stdexcept>
#include <string>
using namespace std;


class CustomException : public exception {
protected:
    string message;
public:
    CustomException(const string& msg) : message(msg) {}

    // Override what() method to provide custom error message
    const char* what() const noexcept override
    {
        return message.c_str();
    }
};


class RepositoryException : public CustomException {
public:
    RepositoryException(const string& msg) : CustomException(msg) {}

    const char* what() const noexcept override
    {
        return message.c_str();
    }

};


class ServiceException : public CustomException {
public:
    ServiceException(const string& msg) : CustomException(msg) {}

    const char* what() const noexcept override
    {
        return message.c_str();
    }
};


class FileException : public CustomException {
public:
    FileException(const string& msg) : CustomException(msg) {}

    const char* what() const noexcept override
    {
        return message.c_str();
    }
};
