#include <iostream>
#include <memory>
#include <string>
using namespace std;

class Channel {
public:
    virtual void send(string message) = 0;
    virtual ~Channel() = default;
};

class Telephone: public Channel {
private:
    string number;
public:
    Telephone(const string &num): number(num) {}
    void send(const string message) override {
        srand(time(NULL));
        int r = rand() % 10;
        if(r == int(number[0] - '0'))
            throw runtime_error("Line is busy");
        cout << message;
    }
    string getNumber() {
        return number;
    }
};

class Fax: public Telephone {
public:
    Fax(const string &num): Telephone(num) {}
    void send(const string message) override {
        Telephone::send(message);
    }
};

class SMS: public Telephone {
public:
    SMS(const string &num): Telephone(num) {}
    void send(const string message) override {
        Telephone::send(message);
    }
};

class FailOver: public Channel{
private:
    Channel *ch1, *ch2;
public:
    FailOver(Channel *ch1, Channel *ch2): ch1(ch1), ch2(ch2) {}
    ~FailOver() {
        delete ch1;
        delete ch2;
    };
    void send(const string message) override {
        try {
            ch1->send(message);
        } catch (runtime_error &e) {
            cout << e.what() << endl;
            ch2->send(message);
        }
    }
};


class Contact {
public:
    Channel *ch1, *ch2, *ch3;
    Contact(Channel *ch1, Channel *ch2, Channel *ch3): ch1(ch1), ch2(ch2), ch3(ch3) {}
    ~Contact() {
        delete ch1;
        delete ch2;
        delete ch3;
    }
    void sendAlarm(const string& message) {
        while(true) {
            try {
                ch1->send(message);
                break;
            }
            catch (runtime_error &e) {
                try {
                    ch2->send(message);
                    break;
                }
                catch (runtime_error &e) {
                    try {
                        ch3->send(message);
                        break;
                    }
                    catch (runtime_error &e) {
                        cout << "All lines are busy" << endl;
                    }
                }
            }
        }
    }
};

Contact* contactFunction(string number) {
    Channel *ch1 = new Telephone(number);
    Channel *ch2 = new FailOver(new Fax(number), new SMS(number));
    Channel *ch3 = new FailOver(new Telephone(number), new FailOver(new Fax(number), new SMS(number)));

    return new Contact(ch1, ch2, ch3);
}

int main() {
    auto contact = contactFunction("112");
    contact->sendAlarm("Hello");

    delete contact;

    return 0;
}