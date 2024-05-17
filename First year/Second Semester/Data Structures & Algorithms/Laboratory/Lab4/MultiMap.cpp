#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <exception>
#include <iostream>

using namespace std;

// BC=WC=TC=Teta(capacity)
MultiMap::MultiMap() : capacity(11), firstEmpty(0), nrElements(0), loadFactor(0.7) {
	elements = new TElem[capacity];
	next = new int[capacity];
	for (int i = 0; i < capacity; i++) {
		elements[i] = NULL_TELEM;
		next[i] = i + 1;
	}
	next[capacity - 1] = -1;
}

//BC=Theta(1), WC=Theta(n), TC=O(n)
void MultiMap::add(TKey c, TValue v) {
	// Check the current load factor
	float currentLoadFactor = (float)nrElements / capacity;

	// Check if the hashtable needs to be resized and rehashed
	if (firstEmpty == capacity || currentLoadFactor >= loadFactor) {
		resizeAndRehash();
	}

	int pos = h(c);

	// If the position is empty
	if (elements[pos] == NULL_TELEM) {
		elements[pos] = make_pair(c, v);
		next[pos] = -1;

		// If this position is the first empty position, update the first empty position
		if (pos == firstEmpty) {
			changeFirstEmpty();
		}
	} else {
		// If the position is not empty, find the next empty position
		int current = pos;
		while (next[current] != -1) {
			current = next[current];
		}

		elements[firstEmpty] = make_pair(c, v);
		next[firstEmpty] = -1;
		next[current] = firstEmpty;

		// Update the first empty position
		changeFirstEmpty();
	}

	nrElements++;
}

//BC=Theta(1), WC=Theta(n), TC=O(n)
void MultiMap::changeFirstEmpty() {
	firstEmpty++;
	while (firstEmpty < capacity && elements[firstEmpty] != NULL_TELEM) {
		firstEmpty++;
	}
}

//BC=Theta(capacity), WC=Theta(capacity), TC=O(capacity)
void MultiMap::resizeAndRehash() {
	// Create new arrays with double the capacity
	auto* newElements = new TElem[capacity * 2];
	auto* newNext = new int[capacity * 2];

	// Initialize the new arrays
	for (int i = 0; i < capacity * 2; i++) {
		newElements[i] = NULL_TELEM;
		newNext[i] = i + 1;
	}
	newNext[capacity * 2 - 1] = -1;

	// Rehash the elements in the old array to the new array
	for (int i = 0; i < capacity; i++) {
		if (elements[i] != NULL_TELEM) {
			TKey c = elements[i].first;
			TValue v = elements[i].second;
			int pos = abs(c) % (capacity * 2); // New hash function with the new capacity
			while (newElements[pos] != NULL_TELEM) {
				pos = newNext[pos];
				if(pos == -1) {
					pos = firstEmpty;
					changeFirstEmpty();
				}
			}
			newElements[pos] = make_pair(c, v);
		}
	}

	// Delete the old arrays
	delete[] elements;
	delete[] next;

	// Update the pointers to the new arrays
	elements = newElements;
	next = newNext;

	// Double the capacity
	capacity *= 2;

	// Update the first empty position
	changeFirstEmpty();
}

// BC=Theta(1), WC=Theta(n), TC=O(n) // n being the number of keys that hash to the same index (collisions)
bool MultiMap::remove(TKey c, TValue v) {
	int pos = h(c);
	int prevPos = -1;
	while (pos != -1 && !(elements[pos].first == c && elements[pos].second == v)) {
		prevPos = pos;
		pos = next[pos];
	}
	if (pos == -1) {
		return false; // element does not exist
	}
	bool over = false;
	do { // moves elements that hash to the same position pos to fill the gap left by the removed element
		int p = next[pos];
		int pp = pos;
		while (p != -1 && h(elements[p].first) != pos) {
			pp = p;
			p = next[p];
		}
		if (p == -1) {
			over = true; // no element hashes to pos
		} else {
			elements[pos] = elements[p]; // move element from position p to pos
			if (next[pp] != -1) {
				next[pp] = next[p];
			}
			pos = p;
		}
	} while (!over);
	// now element from pos can be removed (no element hashes to it)
	if (prevPos == -1) { // the removed element was the first in its linked list
		int idx = 0;
		while (idx < capacity && prevPos == -1) {
			if (next[idx] == pos) {
				prevPos = idx;
			} else {
				idx++;
			}
		}
	}
	if (prevPos != -1) {  // the removed element was not the first in its linked list
		next[prevPos] = next[pos];
	}
	elements[pos] = NULL_TELEM;
	next[pos] = -1;
	if (firstEmpty == -1 || firstEmpty > pos) {
		firstEmpty = pos;
	}
	nrElements--;
	return true;
}

//BC=Theta(1), WC=Theta(n), TC=O(n) // n being the number of keys that hash to the same index (collisions)
vector<TValue> MultiMap::search(TKey c) const {
	vector<TValue> values;
	int i = h(c);
	while (i != -1) {
		if (elements[i].first == c) {
			values.push_back(elements[i].second);
		}
		i = next[i];
	}
	return values;
}

//BC=WC=TC=Theta(1)
int MultiMap::size() const {
	return nrElements;
}

//BC=WC=TC=Theta(1)
bool MultiMap::isEmpty() const {
	return nrElements == 0;
}

//BC=Theta(n), WC=Theta(n^2), TC=O(n^2)
int MultiMap::addIfNotPresent(MultiMap &m) {
	int addedPairs = 0;
	MultiMapIterator it = m.iterator();
	while (it.valid()) {
		TElem current = it.getCurrent();
		if (search(current.first).empty()) { // if the key is not in the MultiMap
			add(current.first, current.second); // add the pair to the MultiMap
			addedPairs++; // increment the number of added pairs
		}
		it.next(); // move to the next pair in the MultiMap
	}
	return addedPairs;
}

//BC=WC=TC=Theta(1)
MultiMapIterator MultiMap::iterator() const {
	return MultiMapIterator(*this);
}

//BC=WC=TC=Theta(1)
MultiMap::~MultiMap() {
	delete[] elements;
	delete[] next;
}

