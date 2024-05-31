#include <exception>
#include "BagIterator.h"
#include "Bag.h"

using namespace std;

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
BagIterator::BagIterator(const Bag& c): bag(c)
{
	first();
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
void BagIterator::first() {
	currentPosition = bag.root;
	currentFrequency = (currentPosition != -1) ? 1 : 0;

	while (currentPosition != -1 && bag.left[currentPosition] != -1) {
		currentPosition = bag.left[currentPosition];
	}
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
void BagIterator::next() {
	if (!valid()) {
		throw exception();
	}

	if (currentFrequency < bag.freq[currentPosition]) {
		currentFrequency++;
	} else {
		currentFrequency = 1;

		if (bag.right[currentPosition] != -1) {
			currentPosition = bag.right[currentPosition];
			while (bag.left[currentPosition] != -1) {
				currentPosition = bag.left[currentPosition];
			}
		} else {
			int parent = bag.parent[currentPosition];
			while (parent != -1 && currentPosition == bag.right[parent]) {
				currentPosition = parent;
				parent = bag.parent[currentPosition];
			}
			currentPosition = parent;
		}
	}
}

// BC=Theta(1), WC=Theta(1), TC=Theta(1)
bool BagIterator::valid() const {
	return currentPosition != -1;
}

// BC=Theta(1), WC=Theta(1), TC=Theta(1)
TElem BagIterator::getCurrent() const
{
	if (!valid()) {
		throw exception();
	}
	return bag.info[currentPosition];
}
