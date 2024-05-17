#pragma once
#include "SortedSet.h"

//DO NOT CHANGE THIS PART
class SortedSetIterator
{
	friend class SortedSet;
private:
	const SortedSet& multime;
	SortedSetIterator(const SortedSet& m);

    int currentElement;

public:
	void first();
	void next();
	TElem getCurrent();
	bool valid() const;
    // changes the current element from the iterator to the previous element, or, if the current element was the first, makes the iterator valid
    // throws an exception if the iterator is not valid
    void previous();
};

