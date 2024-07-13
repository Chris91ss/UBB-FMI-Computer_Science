#pragma once
#include <cassert>
#include <cstring>
#include <string>
#include <stdexcept>
#include <vector>
using namespace std;

template <typename T>
class Stack {
private:
    int capacity;
    vector<T> stack;

public:
    Stack(int cap): capacity(cap) {}
    int getMaxCapacity() {
        return capacity;
    }
    Stack operator+(T item) {
        if(stack.size () >= capacity) {
            throw runtime_error("Stack is full!");
        }
        stack.push_back(item);
        return *this;
    }
    T pop() {
        if(stack.size() == 0) {
            throw runtime_error("Stack is empty!");
        }
        T item = stack.back();
        stack.pop_back();
        return item;
    }
};