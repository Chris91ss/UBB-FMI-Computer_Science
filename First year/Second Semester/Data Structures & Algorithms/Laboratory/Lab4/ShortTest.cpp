#include "ShortTest.h"
#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <assert.h>
#include <vector>
#include<iostream>
#include <map>

void testAll() {
	MultiMap m;
	m.add(1, 100);
	m.add(2, 200);
	m.add(3, 300);
	m.add(1, 500);
	m.add(2, 600);
	m.add(4, 800);

	assert(m.size() == 6);

	assert(m.remove(5, 600) == false);
	assert(m.remove(1, 500) == true);

	assert(m.size() == 5);

    vector<TValue> v;
	v=m.search(6);
	assert(v.size()==0);

	v=m.search(1);
	assert(v.size()==1);

	assert(m.isEmpty() == false);

	MultiMapIterator im = m.iterator();
	assert(im.valid() == true);
	while (im.valid()) {
		im.getCurrent();
		im.next();
	}
	assert(im.valid() == false);
	im.first();
	assert(im.valid() == true);

	// test function addIfNotPresent
	MultiMap m2;
	m2.add(10, 1070);
	m2.add(11, 2542);
	m2.add(12, 2956);
	int addedPairs = m.addIfNotPresent(m2);
	assert(addedPairs == 3);
	assert(m.size() == 8);
	m2.add(13, 525);
	m2.add(14, 654);
	addedPairs = m.addIfNotPresent(m2);
	assert(addedPairs == 2);
	assert(m.size() == 10);
	m2.add(1, 101);
	addedPairs = m.addIfNotPresent(m2);
	assert(addedPairs == 0);
	assert(m.size() == 10);
}
