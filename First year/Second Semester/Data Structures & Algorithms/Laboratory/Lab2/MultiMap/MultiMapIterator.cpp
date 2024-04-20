#include "MultiMapIterator.h"
#include "MultiMap.h"

// BC = WC = TC = Theta(1)
MultiMapIterator::MultiMapIterator(const MultiMap& c): col(c) {
    currentNode = col.list.head;
}

// BC = WC = TC = Theta(1)
TElem MultiMapIterator::getCurrent() const{
    if(currentNode == nullptr)
        throw exception();
    return currentNode->info;
}

// BC = WC = TC = Theta(1)
bool MultiMapIterator::valid() const {
    return currentNode != nullptr;
}

// BC = WC = TC = Theta(1)
void MultiMapIterator::next() {
    if(currentNode == nullptr)
        throw exception();
    currentNode = currentNode->next;
}

// BC = WC = TC = Theta(1)
void MultiMapIterator::first() {
    currentNode = col.list.head;
}

