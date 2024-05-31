#include "Bag.h"
#include "BagIterator.h"
#include <exception>
#include <iostream>
using namespace std;

// BC=WC=TC=Theta(capacity)
void Bag::resize() {
	int newCapacity = capacity * 2;
	TElem* newInfo = new TElem[newCapacity];
	int* newLeft = new int[newCapacity];
	int* newRight = new int[newCapacity];
	int* newParent = new int[newCapacity];
	int* newFreq = new int[newCapacity];

	for (int i = 0; i < capacity; i++) {
		newInfo[i] = info[i];
		newLeft[i] = left[i];
		newRight[i] = right[i];
		newParent[i] = parent[i];
		newFreq[i] = freq[i];
	}

	for (int i = capacity; i < newCapacity - 1; i++) {
		newLeft[i] = i + 1;
		newRight[i] = -1;
		newParent[i] = -1;
		newFreq[i] = 0;
	}
	newLeft[newCapacity - 1] = -1;
	newRight[newCapacity - 1] = -1;
	newParent[newCapacity - 1] = -1;
	newFreq[newCapacity - 1] = 0;

	delete[] info;
	delete[] left;
	delete[] right;
	delete[] parent;
	delete[] freq;

	info = newInfo;
	left = newLeft;
	right = newRight;
	parent = newParent;
	freq = newFreq;
	firstEmpty = capacity;
	capacity = newCapacity;
}

// BC=Theta(1), WC=Theta(capacity), TC=Theta(capacity)
int Bag::createNode(TElem elem) {
	if (firstEmpty == -1) {
		resize();
	}

	int newNode = firstEmpty;
	firstEmpty = left[firstEmpty];

	info[newNode] = elem;
	left[newNode] = -1;
	right[newNode] = -1;
	parent[newNode] = -1;
	freq[newNode] = 1;

	return newNode;
}

// BC=WC=TC=Theta(capacity)
Bag::Bag() {
	capacity = 10;
	info = new TElem[capacity];
	left = new int[capacity];
	right = new int[capacity];
	parent = new int[capacity];
	freq = new int[capacity];
	root = -1;
	firstEmpty = 0;

	for (int i = 0; i < capacity - 1; i++) {
		left[i] = i + 1;
		right[i] = -1;
		parent[i] = -1;
		freq[i] = 0;
	}
	left[capacity - 1] = -1;
	right[capacity - 1] = -1;
	parent[capacity - 1] = -1;
	freq[capacity - 1] = 0;
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
void Bag::add(TElem elem) {
	if (root == -1) {
		root = createNode(elem);
		return;
	}

	int currentNode = root;
	int parentNode = -1;

	while (currentNode != -1) {
		parentNode = currentNode;
		if (info[currentNode] == elem) {
			freq[currentNode]++;
			return;
		} if (info[currentNode] > elem) {
			currentNode = left[currentNode];
		} else {
			currentNode = right[currentNode];
		}
	}

	int newNode = createNode(elem);
	parent[newNode] = parentNode;

	if (info[parentNode] > elem) {
		left[parentNode] = newNode;
	} else {
		right[parentNode] = newNode;
	}
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
bool Bag::remove(TElem elem) {
	int currentNode = root;
    int parentNode = -1;
    while (currentNode != -1 && info[currentNode] != elem) {
        parentNode = currentNode;
        if (info[currentNode] > elem) {
            currentNode = left[currentNode];
        } else {
            currentNode = right[currentNode];
        }
    }

    if (currentNode == -1) {
        return false;
    }

    if (freq[currentNode] > 1) {
        freq[currentNode]--;
        return true;
    }

    if (left[currentNode] == -1 && right[currentNode] == -1) {
        if (currentNode == root) {
            root = -1;
        } else {
            if (left[parentNode] == currentNode) {
                left[parentNode] = -1;
            } else {
                right[parentNode] = -1;
            }
        }
    } else if (left[currentNode] == -1 || right[currentNode] == -1) {
        int childNode = (left[currentNode] != -1) ? left[currentNode] : right[currentNode];
        if (currentNode == root) {
            root = childNode;
        } else {
            if (left[parentNode] == currentNode) {
                left[parentNode] = childNode;
            } else {
                right[parentNode] = childNode;
            }
            parent[childNode] = parentNode;
        }
    } else {
        int replacementNode = right[currentNode];
        int replacementParent = currentNode;

        while (left[replacementNode] != -1) {
            replacementParent = replacementNode;
            replacementNode = left[replacementNode];
        }

        info[currentNode] = info[replacementNode];
        freq[currentNode] = freq[replacementNode];

        if (replacementParent != currentNode) {
            left[replacementParent] = right[replacementNode];
        } else {
            right[replacementParent] = right[replacementNode];
        }

        if (right[replacementNode] != -1) {
            parent[right[replacementNode]] = replacementParent;
        }

        currentNode = replacementNode;
    }

    left[currentNode] = firstEmpty;
    firstEmpty = currentNode;

    return true;
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
bool Bag::search(TElem elem) const {
	int currentNode = root;

	while (currentNode != -1) {
		if (info[currentNode] == elem) {
			return true;
		} if (info[currentNode] > elem) {
			currentNode = left[currentNode];
		} else {
			currentNode = right[currentNode];
		}
	}

	return false;
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
int Bag::nrOccurrences(TElem elem) const {
	int currentNode = root;

	while (currentNode != -1) {
		if (info[currentNode] == elem) {
			return freq[currentNode];
		} if (info[currentNode] > elem) {
			currentNode = left[currentNode];
		} else {
			currentNode = right[currentNode];
		}
	}

	return 0;
}

// BC=Theta(1), WC=Theta(n), TC=Theta(n)
int Bag::size() const {
	int count = 0;
	int currentNode = root;
	int stack[capacity];
	int top = -1;

	// Perform an in-order traversal to count the number of elements
	while (currentNode != -1 || top != -1) {
		while (currentNode != -1) {
			stack[++top] = currentNode;
			currentNode = left[currentNode];
		}

		currentNode = stack[top--];
		count += freq[currentNode];
		currentNode = right[currentNode];
	}

	return count;
}

// BC=WC=TC=Theta(1)
bool Bag::isEmpty() const {
	return root == -1;
}

// BC=WC=TC=Theta(1)
BagIterator Bag::iterator() const {
	return BagIterator(*this);
}

// BC=WC=TC=Theta(1)
Bag::~Bag() {
	delete[] info;
	delete[] left;
	delete[] right;
	delete[] parent;
	delete[] freq;
}

