#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <memory>
using namespace std;

// Abstract class Encoder
class Encoder {
public:
    virtual string encode(const string& msg) = 0; // Pure virtual function
    virtual ~Encoder() = default;
};

// AlienEncoder class
class AlienEncoder : public Encoder {
private:
    string header;
public:
    AlienEncoder(const string& header) : header(header) {}
    string encode(const string& msg) override {
        return header + msg;
    }
};

// MorseEncoder class
class MorseEncoder : public Encoder {
public:
    string encode(const string& msg) override {
        string encodedMsg;
        for (char c : msg) {
            encodedMsg += ".";
        }
        return encodedMsg;
    }
};

// Mixer class
class Mixer : public Encoder {
private:
    Encoder* encoder1;
    Encoder* encoder2;
public:
    Mixer(Encoder* e1, Encoder* e2) : encoder1(e1), encoder2(e2) {}
    string encode(const string& msg) override {
        string encoded1 = encoder1->encode(msg);
        string encoded2 = encoder2->encode(msg);
        string mixedMsg;
        for (size_t i = 0; i < encoded1.size() && i < encoded2.size(); ++i) {
            mixedMsg += encoded1[i];
            mixedMsg += encoded2[i];
        }
        return mixedMsg;
    }
};

// Communication class
class Communication {
private:
    vector<string> messages;
    Encoder* encoder;
public:
    Communication(Encoder* e) : encoder(e) {}
    void addMessage(const string& msg) {
        messages.push_back(msg);
    }
    void communicate() {
        // Sort messages alphabetically
        sort(messages.begin(), messages.end());
        // Encode and output each message
        for (const string& msg : messages) {
            cout << encoder->encode(msg) << endl;
        }
    }
};

int main() {
    // Create encoders
    AlienEncoder alienEncoder("ET");
    MorseEncoder morseEncoder;
    Mixer mixer(&alienEncoder, &morseEncoder);

    // Create communication objects
    Communication com1(&morseEncoder);
    Communication com2(&mixer);

    // Add messages
    com1.addMessage("hello");
    com1.addMessage("world");
    com2.addMessage("hello");
    com2.addMessage("world");

    // Communicate
    cout << "Communication 1:" << endl;
    com1.communicate();

    cout << "Communication 2:" << endl;
    com2.communicate();

    return 0;
}
