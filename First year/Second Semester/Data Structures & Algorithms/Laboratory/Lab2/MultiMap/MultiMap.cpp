#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <exception>
#include <iostream>

using namespace std;

// BC = WC = TC = Theta(1)
MultiMap::MultiMap() {
	list.head = nullptr;
    list.tail = nullptr;
    length = 0;
}

// BC = WC = TC = Theta(1)
void MultiMap::add(TKey c, TValue v) {
    // Create a new node with the given key-value pair
    auto* newNode = new DLLNode(TElem(c, v));

    // If the list is empty, set both head and tail to the new node
    if (list.head == nullptr) {
        list.head = newNode;
        list.tail = newNode;
    } else {
        // Otherwise, add the new node to the end of the list
        list.tail->next = newNode;
        newNode->prev = list.tail;
        list.tail = newNode;
    }

    // Increment the length of the list
    length++;
}

// BC = Theta(1), WC = Theta(length), TC = Theta(length)
bool MultiMap::remove(TKey c, TValue v) {
    // Start from the head of the list
    auto* currentNode = list.head;

    // Iterate through the list
    while (currentNode != nullptr) {
        // If the current node has the key-value pair we're looking for
        if (currentNode->info.first == c && currentNode->info.second == v) {
            // If the current node is the head of the list
            if (currentNode == list.head) {
                // Move the head to the next node
                list.head = currentNode->next;

                // If the head is not null, set its previous pointer to null
                if (list.head != nullptr) {
                    list.head->prev = nullptr;
                }
            } else {
                // Otherwise, set the previous node's next pointer to the current node's next pointer
                currentNode->prev->next = currentNode->next;

                // If the current node is not the tail of the list
                if (currentNode->next != nullptr) {
                    // Set the next node's previous pointer to the current node's previous pointer
                    currentNode->next->prev = currentNode->prev;
                } else {
                    // Otherwise, set the tail to the previous node
                    list.tail = currentNode->prev;
                }
            }

            // Delete the current node
            delete currentNode;

            // Decrement the length of the list
            length--;

            // Return true, as we found and removed the key-value pair
            return true;
        }

        // Move to the next node
        currentNode = currentNode->next;
    }

    // If we didn't find the key-value pair, return false
    return false;
}

// BC = WC = TC = Theta(length)
vector<TValue> MultiMap::search(TKey c) const {
    // Create a vector to store the values associated with the given key
    vector<TValue> values;

    // Start from the head of the list
    auto* currentNode = list.head;

    // Iterate through the list
    while (currentNode != nullptr) {
        // If the current node has the key we're looking for
        if (currentNode->info.first == c) {
            // Add the value to the vector
            values.push_back(currentNode->info.second);
        }

        // Move to the next node
        currentNode = currentNode->next;
    }

    // Return the vector of values
    return values;
}

// BC = WC = TC = Theta(1)
int MultiMap::size() const {
    // Return the length of the list
    return length;
}

// BC = WC = TC = Theta(1)
bool MultiMap::isEmpty() const {
    // Return whether the list is empty
    return length == 0;
}

// BC = WC = TC = Theta(length)
void MultiMap::filter(bool (*condition)(TKey)) {
    // Start from the head of the list
    auto* currentNode = list.head;

    // Iterate through the list
    while (currentNode != nullptr) {
        // Save the next node
        auto* nextNode = currentNode->next;

        // If the key of the current node does not respect the condition
        if (!condition(currentNode->info.first)) {
            // If the current node is the head of the list
            if (currentNode == list.head) {
                // Move the head to the next node
                list.head = currentNode->next;

                // If the head is not null, set its previous pointer to null
                if (list.head != nullptr) {
                    list.head->prev = nullptr;
                }
            } else {
                // Otherwise, set the previous node's next pointer to the current node's next pointer
                currentNode->prev->next = currentNode->next;

                // If the current node is not the tail of the list
                if (currentNode->next != nullptr) {
                    // Set the next node's previous pointer to the current node's previous pointer
                    currentNode->next->prev = currentNode->prev;
                } else {
                    // Otherwise, set the tail to the previous node
                    list.tail = currentNode->prev;
                }
            }

            // Delete the current node
            delete currentNode;

            // Decrement the length of the list
            length--;
        }

        // Move to the next node
        currentNode = nextNode;
    }
}

// BC = WC = TC = Theta(1)
MultiMapIterator MultiMap::iterator() const {
	return MultiMapIterator(*this);
}

// BC = WC = TC = Theta(length)
MultiMap::~MultiMap() {
    // Start from the head of the list
    auto* currentNode = list.head;

    // Iterate through the list
    while (currentNode != nullptr) {
        // Save the next node
        auto* nextNode = currentNode->next;

        // Delete the current node
        delete currentNode;

        // Move to the next node
        currentNode = nextNode;
    }
    list.head = nullptr;
    list.tail = nullptr;
    length = 0;
}

