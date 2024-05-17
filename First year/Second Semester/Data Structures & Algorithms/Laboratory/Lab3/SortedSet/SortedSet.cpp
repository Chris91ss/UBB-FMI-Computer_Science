#include "SortedSet.h"
#include "SortedSetIterator.h"
#include <algorithm>
using namespace std;

// BC=WC=AC=Theta(n) where n is the initial capacity
SortedSet::SortedSet(Relation r) {
    this->r = r;
    this->cap = 10;
    this->setSize = 0;
    this->head = -1;
    this->firstEmpty = 0;
    this->elems = new TElem[cap];
    this->next = new int[cap];
    fill_n(this->next, cap, -1);
    for (int i = 0; i < cap - 1; i++)
        this->next[i] = i + 1;
}

//BC=WC=AC=Theta(n) where n is the number of elements in the set
void SortedSet::resize() {
    auto* newElems = new TElem[cap * 2];
    int* newNext = new int[cap * 2];
    copy(elems, elems + cap, newElems);
    copy(next, next + cap, newNext);
    fill(newNext + cap, newNext + cap * 2, -1);
    for (int i = cap; i < cap * 2 - 1; i++)
        newNext[i] = i + 1;
    firstEmpty = cap;
    cap *= 2;
    delete[] elems;
    delete[] next;
    elems = newElems;
    next = newNext;
}

//BC=Theta(1) WC=Theta(n) AC=O(n) where n is the number of elements in the set
bool SortedSet::add(TComp e) {
    if (search(e))
        return false;
    if (firstEmpty == -1)
        resize();
    int current = head, prev = -1;
    while (current != -1 && r(elems[current], e)) {
        prev = current;
        current = next[current];
    }
    int newElem = firstEmpty;
    firstEmpty = next[firstEmpty];
    elems[newElem] = e;
    next[newElem] = current;
    if (prev == -1)
        head = newElem;
    else
        next[prev] = newElem;
    setSize++;
    return true;
}

//BC=Theta(1) WC=Theta(n) AC=O(n) where n is the number of elements in the set
bool SortedSet::remove(TComp e) {
    if (!search(e))
        return false;
    int current = head, prev = -1;
    while (elems[current] != e) {
        prev = current;
        current = next[current];
    }
    if (prev == -1)
        head = next[head];
    else
        next[prev] = next[current];
    next[current] = firstEmpty;
    firstEmpty = current;
    setSize--;
    return true;
}

//BC=WC=AC=O(n) where n is the number of elements in the set
bool SortedSet::search(TElem elem) const {
    int current = head;
    while (current != -1) {
        if (elems[current] == elem)
            return true;
        current = next[current];
    }
    return false;
}

//BC=WC=AC=Theta(1)
int SortedSet::size() const {
    return setSize;
}

//BC=WC=AC=Theta(1)
bool SortedSet::isEmpty() const {
    return head == -1;
}

//BC=WC=AC=Theta(1)
SortedSetIterator SortedSet::iterator() const {
	return SortedSetIterator(*this);
}

//BC=WC=AC=Theta(1)
SortedSet::~SortedSet() {
    delete[] elems;
    delete[] next;
}
