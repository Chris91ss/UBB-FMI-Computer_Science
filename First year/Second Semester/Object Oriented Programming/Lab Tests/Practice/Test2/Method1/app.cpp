#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <ctime>

// MedicalAnalysis abstract class
class MedicalAnalysis {
public:
    std::string date;
    virtual bool isResultOK() const = 0;
    virtual std::string toString() const = 0;
    virtual ~MedicalAnalysis() {}
};

// BMI class derived from MedicalAnalysis
class BMI : public MedicalAnalysis {
public:
    double value;
    BMI(const std::string &date, double value) : value(value) { this->date = date; }
    bool isResultOK() const override { return value >= 18.5 && value <= 25; }
    std::string toString() const override {
        return "BMI analysis on " + date + ": value = " + std::to_string(value) +
               ", result is " + (isResultOK() ? "OK" : "Not OK");
    }
};

// BP class derived from MedicalAnalysis
class BP : public MedicalAnalysis {
public:
    int systolicValue;
    int diastolicValue;
    BP(const std::string &date, int systolicValue, int diastolicValue) :
            systolicValue(systolicValue), diastolicValue(diastolicValue) { this->date = date; }
    bool isResultOK() const override {
        return systolicValue >= 90 && systolicValue <= 119 &&
               diastolicValue >= 60 && diastolicValue <= 79;
    }
    std::string toString() const override {
        return "BP analysis on " + date + ": systolic = " + std::to_string(systolicValue) +
               ", diastolic = " + std::to_string(diastolicValue) +
               ", result is " + (isResultOK() ? "OK" : "Not OK");
    }
};

// Person class
class Person {
private:
    std::string name;
    std::vector<MedicalAnalysis*> analyses;

public:
    explicit Person(std::string name) : name(std::move(name)) {}
    ~Person() {
        for (auto analysis : analyses) {
            delete analysis;
        }
    }

    void addAnalysis(MedicalAnalysis* analysis) {
        analyses.push_back(analysis);
    }

    const std::vector<MedicalAnalysis*>& getAllAnalyses() const {
        return analyses;
    }

    std::vector<MedicalAnalysis*> getAnalysesByMonth(int month) const {
        std::vector<MedicalAnalysis*> monthlyAnalyses;
        for (auto* analysis : analyses) {
            int analysisMonth = std::stoi(analysis->date.substr(5, 2));
            if (analysisMonth == month) {
                monthlyAnalyses.push_back(analysis);
            }
        }
        return monthlyAnalyses;
    }

    bool isIll(int month) const {
        auto monthlyAnalyses = getAnalysesByMonth(month);
        for (auto* analysis : monthlyAnalyses) {
            if (analysis->isResultOK()) {
                return false;
            }
        }
        return true;
    }

    std::vector<MedicalAnalysis*> getAnalysesBetweenDates(const std::string& date1, const std::string& date2) const {
        std::vector<MedicalAnalysis*> filteredAnalyses;
        for (auto* analysis : analyses) {
            if (analysis->date >= date1 && analysis->date <= date2) {
                filteredAnalyses.push_back(analysis);
            }
        }
        return filteredAnalyses;
    }

    void writeToFile(const std::string& filename, const std::string& date1, const std::string& date2) {
        std::ofstream file(filename);
        if (!file) {
            std::cerr << "Could not open file for writing.\n";
            return;
        }

        auto filteredAnalyses = getAnalysesBetweenDates(date1, date2);
        for (auto* analysis : filteredAnalyses) {
            file << analysis->toString() << '\n';
        }

        file.close();
    }
};

#include <limits>

class UI {
private:
    Person &person;

    // Utility function to clear standard input
    void clearInput() {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    // Function to add a new analysis
    void addNewAnalysis() {
        std::cout << "Enter the type of analysis (BMI or BP): ";
        std::string type;
        std::cin >> type;
        clearInput();

        std::string date;
        std::cout << "Enter the date of analysis (yyyy.mm.dd): ";
        std::cin >> date;
        clearInput();

        if (type == "BMI") {
            double value;
            std::cout << "Enter the BMI value: ";
            std::cin >> value;
            clearInput();
            person.addAnalysis(new BMI(date, value));
        } else if (type == "BP") {
            int systolic, diastolic;
            std::cout << "Enter the systolic and diastolic values: ";
            std::cin >> systolic >> diastolic;
            clearInput();
            person.addAnalysis(new BP(date, systolic, diastolic));
        } else {
            std::cout << "Invalid analysis type.\n";
        }
    }

    // Function to print all analyses
    void printAllAnalyses() {
        for (const auto *analysis : person.getAllAnalyses()) {
            std::cout << analysis->toString() << std::endl;
        }
    }

    // Function to check if the person is ill in a given month
    void checkIfIll() {
        int month;
        std::cout << "Enter the current month (as an integer): ";
        std::cin >> month;
        clearInput();
        if (person.isIll(month)) {
            std::cout << "The person is ill.\n";
        } else {
            std::cout << "The person is not ill.\n";
        }
    }

    // Function to write analyses to a file between two dates
    void writeAnalysesToFile() {
        std::string filename, date1, date2;
        std::cout << "Enter the filename: ";
        std::cin >> filename;
        clearInput();
        std::cout << "Enter the start date (yyyy.mm.dd): ";
        std::cin >> date1;
        clearInput();
        std::cout << "Enter the end date (yyyy.mm.dd): ";
        std::cin >> date2;
        clearInput();
        person.writeToFile(filename, date1, date2);
        std::cout << "Data written to " << filename << std::endl;
    }

public:
    explicit UI(Person &person) : person(person) {}

    // Function to run the UI
    void run() {
        while (true) {
            std::cout << "Medical Analysis Application\n";
            std::cout << "1. Add a new analysis\n";
            std::cout << "2. Show all analyses\n";
            std::cout << "3. Check if ill\n";
            std::cout << "4. Write analyses to file\n";
            std::cout << "5. Exit\n";
            std::cout << "Enter option: ";
            int option;
            std::cin >> option;
            clearInput();

            switch (option) {
                case 1:
                    addNewAnalysis();
                    break;
                case 2:
                    printAllAnalyses();
                    break;
                case 3:
                    checkIfIll();
                    break;
                case 4:
                    writeAnalysesToFile();
                    break;
                case 5:
                    std::cout << "Exiting application.\n";
                    return;
                default:
                    std::cout << "Invalid option. Please try again.\n";
            }
        }
    }
};
// Service and UI layers will go here

int main() {
    // Initialization of the application and test data
    Person person("John Doe");
    person.addAnalysis(new BMI("2024.04.15", 22.5));
    person.addAnalysis(new BP("2024.03.30", 115, 75));

    UI ui(person);
    ui.run();
    // The rest of the UI and Service code will handle user interaction
    // and use the Person class to perform operations as needed.

    return 0;
}