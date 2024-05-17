#include "SortedSetIterator.h"
#include <exception>

using namespace std;

//BC=WC=AC=Theta(1)
SortedSetIterator::SortedSetIterator(const SortedSet& m) : multime(m)
{
	currentElement = multime.head;
}

//BC=WC=AC=Theta(1)
void SortedSetIterator::first() {
    currentElement = multime.head;
}

//BC=WC=AC=Theta(1)
void SortedSetIterator::next() {
    if (!valid()) {
        throw exception();
    }
    currentElement = multime.next[currentElement];
}

//BC=WC=AC=Theta(1)
TElem SortedSetIterator::getCurrent()
{
    if (!valid()) {
        throw exception();
    }
    return multime.elems[currentElement];
}

//BC=WC=AC=Theta(1)
bool SortedSetIterator::valid() const {
    return currentElement != -1;
}

//BC=Theta(1) WC=Theta(n) AC=O(n) where n is the number of elements in the set
void SortedSetIterator::previous() {
    if (!valid()) {
        throw exception();
    }
    int prev = -1;
    int current = multime.head;
    while (current != currentElement) {
        prev = current;
        current = multime.next[current];
    }
    currentElement = prev;
}


