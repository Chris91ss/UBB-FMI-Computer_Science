#include "ShortTest.h"
#include <assert.h>
#include "Map.h"
#include "MapIterator.h"


void testAll() { //call each function to see if it is implemented
	Map m;
	assert(m.isEmpty() == true);
	assert(m.size() == 0); //add elements
	assert(m.add(5,5)==NULL_TVALUE);
	assert(m.add(1,111)==NULL_TVALUE);
	assert(m.add(10,110)==NULL_TVALUE);
	assert(m.add(7,7)==NULL_TVALUE);
	assert(m.add(1,1)==111);
	assert(m.add(10,10)==110);
	assert(m.add(-3,-3)==NULL_TVALUE);
	assert(m.size() == 5);
	assert(m.search(10) == 10);
	assert(m.search(16) == NULL_TVALUE);
	assert(m.remove(1) == 1);
	assert(m.remove(6) == NULL_TVALUE);
	assert(m.size() == 4);


	TElem e;
	MapIterator id = m.iterator();
	id.first();
	int s1 = 0, s2 = 0;
	while (id.valid()) {
		e = id.getCurrent();
		s1 += e.first;
		s2 += e.second;
		id.next();
	}
	assert(s1 == 19);
	assert(s2 == 19);

    Map m1;
    assert(m1.isEmpty() == true);
    assert(m1.size() == 0);
    assert(m1.getValueRange() == -1);
    assert(m1.add(1, 3) == NULL_TVALUE);
    assert(m1.add(2, 10) == NULL_TVALUE);
    assert(m1.getValueRange() == 7);
    assert(m1.add(3, 1) == NULL_TVALUE);
    assert(m1.getValueRange() == 9);

    Map m2;
    assert(m2.isEmpty() == true);
    assert(m2.size() == 0);
    assert(m2.getValueRange() == -1);
    assert(m2.add(1, 100) == NULL_TVALUE);
    assert(m2.add(2, 250) == NULL_TVALUE);
    assert(m2.add(3, 1000) == NULL_TVALUE);
    assert(m2.getValueRange() == 900);

    Map m3;
    assert(m3.isEmpty() == true);
    assert(m3.size() == 0);
    assert(m3.getValueRange() == -1);
    assert(m3.add(1, 100) == NULL_TVALUE);
    assert(m3.add(1, 250) == 100);
    assert(m3.add(3, 1000) == NULL_TVALUE);
    assert(m3.add(3, 5000) == 1000);
    assert(m3.getValueRange() == 4750);
}


