//
// Created by qdeni on 6/27/2023.
//

#ifndef DRIVE_MESSAGE_H
#define DRIVE_MESSAGE_H

#include <string>

class Message {
private:
    std::string text;
    std::string sender;
    std::string time;

public:
    Message() = default;

    Message(const std::string &text, const std::string &sender, const std::string &time) : text(text), sender(sender),
                                                                                           time(time) {};

    std::string getText() const {
        return this->text;
    }

    std::string getSender() const {
        return this->sender;
    }

    std::string getTime() const {
        return this->time;
    }

    std::string toString() const {
        return this->sender + "(" + this->time + "): " + this->text;
    }
};


#endif //DRIVE_MESSAGE_H
