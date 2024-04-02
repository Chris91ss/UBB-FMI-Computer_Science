#include "Map.h"
#include "MapIterator.h"
#include <exception>
using namespace std;

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
MapIterator::MapIterator(const Map& d) : map(d)
{
	this->currentPosition = 0;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
void MapIterator::first() {
	this->currentPosition = 0;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
void MapIterator::next() {
	if(!this->valid())
        throw exception();
    this->currentPosition++;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
TElem MapIterator::getCurrent(){
    if(!this->valid())
        throw exception();
    return this->map.elements[this->currentPosition];
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
bool MapIterator::valid() const {
    return this->currentPosition < this->map.mapSize;
}



