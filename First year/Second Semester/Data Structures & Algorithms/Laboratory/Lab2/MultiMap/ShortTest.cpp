#include "ShortTest.h"
#include "MultiMap.h"
#include "MultiMapIterator.h"
#include <assert.h>
#include <vector>
#include<iostream>

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



    MultiMap m1;
    m1.add(1, 100);
    m1.add(2, 200);
    m1.add(3, 300);
    m1.add(1, 500);
    m1.add(2, 600);
    m1.add(4, 800);
    m1.filter([](TKey key) { return key % 2 == 0; });
    assert(m1.size() == 3);
    assert(m1.search(1).size() == 0);
    assert(m1.search(2).size() == 2);
    assert(m1.search(3).size() == 0);
    assert(m1.search(4).size() == 1);
    assert(m1.search(5).size() == 0);
    assert(m1.search(6).size() == 0);

    MultiMap m2;
    m1.add(1, 100);
    m1.add(2, 200);
    m1.add(3, 300);
    m1.add(1, 500);
    m1.add(2, 600);
    m1.add(4, 800);
    m1.filter([](TKey key) { return key % 2 == 1; });
    assert(m1.size() == 3);
    assert(m1.search(1).size() == 2);
    assert(m1.search(2).size() == 0);
    assert(m1.search(3).size() == 1);
    assert(m1.search(4).size() == 0);
    assert(m1.search(5).size() == 0);
    assert(m1.search(6).size() == 0);
}
