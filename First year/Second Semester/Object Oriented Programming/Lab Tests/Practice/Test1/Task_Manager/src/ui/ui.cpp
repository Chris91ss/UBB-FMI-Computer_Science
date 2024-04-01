#include "ui/ui.h"

UI::UI(Service &service) : service(service) {
    this->service.Generate5Tasks();
}

UI::~UI() = default;

void UI::Run() {
    try {
        while (true) {
            PrintMenu();
            int command;
            cout << ">Command: ";
            cin >> command;
            try {
                switch (command) {
                    case 1: {
                        AddTaskUI();
                        break;
                    }
                    case 2: {
                        DisplayTasksUI();
                        break;
                    }
                    case 3: {
                        DisplayFilteredAndSortedTasksUI();
                        break;
                    }
                    default: {
                        cout << "Invalid command\n";
                        break;
                    }
                }
            }
            catch (exception &exception) {
                cout << exception.what();
            }
        }
    }
    catch (exception &exception) {
        cout << exception.what();
    }
}

void UI::PrintMenu() {
    cout << "1. Add task\n";
    cout << "2. Display tasks\n";
    cout << "3. Display filtered and sorted tasks\n";
}

void UI::AddTaskUI() {
    string description;
    int duration, priority;
    cout << "Description: ";
    cin >> description;
    cout << "Duration: ";
    cin >> duration;
    cout << "Priority: ";
    cin >> priority;
    this->service.AddTask(description, duration, priority);

    cout << "Task added successfully \n";
}

void UI::DisplayTasksUI() {
    DynamicVector<Task> tasks = this->service.GetAllTasks();
    for (int i = 0; i < tasks.GetSizeOfDynamicVector(); i++) {
        Task task = tasks[i];
        cout << task.getDescription() << " | " << task.getDuration() << " | " << task.getPriority() << "\n";
    }
}

void UI::DisplayFilteredAndSortedTasksUI() {
    int priority;
    cout << "Priority: ";
    cin >> priority;
    DynamicVector<Task> tasks = this->service.GetTasksFilteredAndSorted(priority);
    for (int i = 0; i < tasks.GetSizeOfDynamicVector(); i++) {
        Task task = tasks[i];
        cout << task.getDescription() << " | " << task.getDuration() << " | " << task.getPriority() << "\n";
    }
}
