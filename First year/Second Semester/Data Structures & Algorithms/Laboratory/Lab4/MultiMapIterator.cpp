#include "MultiMapIterator.h"
#include "MultiMap.h"

// BC=WC=Theta(capacity) TC=O(capacity)
MultiMapIterator::MultiMapIterator(const MultiMap& c): col(c), currentPos(0) {
	while (currentPos < col.capacity && col.elements[currentPos] == NULL_TELEM) {
		currentPos++;
	}
}

// BC=WC=TC=Theta(1)
TElem MultiMapIterator::getCurrent() const{
	if (!valid() || col.nrElements == 0) {
		throw exception();
	}
	return col.elements[currentPos];
}

// BC=WC=TC=Theta(1)
bool MultiMapIterator::valid() const {
	return currentPos < col.capacity;
}

// BC=WC=Theta(capacity) TC=O(capacity)
void MultiMapIterator::next() {
	if (!valid()) {
		throw exception();
	}
	currentPos++;
	while (currentPos < col.capacity && col.elements[currentPos] == NULL_TELEM) {
		currentPos++;
	}
}

// BC=WC=Theta(capacity) TC=O(capacity)
void MultiMapIterator::first() {
	currentPos = 0;
	while (currentPos < col.capacity && col.elements[currentPos] == NULL_TELEM) {
		currentPos++;
	}
}

