#include "Map.h"
#include "MapIterator.h"

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
Map::Map() {
    this->capacity = 2;
    this->mapSize = 0;
    this->elements = new TElem[capacity];
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
Map::~Map() {
	delete[] this->elements;
}

//BC: Theta(mapSize), WC: Theta(mapSize), TC: Theta(mapSize)
void Map::resize(){
    TElem* newElements = new TElem[this->capacity];
    for(int i = 0; i < this->mapSize; i++)
        newElements[i] = this->elements[i];
    delete[] this->elements;
    this->elements = newElements;
}

//BC: Theta(1) - when the first key from the map is equal to c
//WC: Theta(mapSize) - when the key c is not in the map
//TC: O(mapSize)
TValue Map::add(TKey c, TValue v){
    if(this->mapSize == this->capacity) {
        this->capacity *= 2;
        this->resize();
    }

    for(int i = 0; i < this->mapSize; i++)
        if(this->elements[i].first == c)
        {
            TValue oldValue = this->elements[i].second;
            this->elements[i].second = v;
            return oldValue;
        }

    this->elements[this->mapSize].first = c;
    this->elements[this->mapSize].second = v;
    this->mapSize++;

	return NULL_TVALUE;
}

//BC: Theta(1) - when the first key from the map is equal to c
//WC: Theta(mapSize) - when the key c is not in the map
//TC: O(mapSize)
TValue Map::search(TKey c) const{
	for(int i = 0; i < this->mapSize; i++)
        if(this->elements[i].first == c)
            return this->elements[i].second;

	return NULL_TVALUE;
}

//BC: Theta(mapSize) - when the first key from the map is equal to c
//WC: Theta(mapSize) - when the key c is not in the map
//TC: O(mapSize)
TValue Map::remove(TKey c){
	for(int i = 0; i < this->mapSize; i++)
        if(this->elements[i].first == c)
        {
            TValue oldValue = this->elements[i].second;
            for(int j = i; j < this->mapSize - 1; j++)
                this->elements[j] = this->elements[j + 1];
            this->mapSize--;
            return oldValue;
        }
    if(this->mapSize < this->capacity / 4 && this->capacity > 4)
    {
        this->capacity /= 2;
        this->resize();
    }
	return NULL_TVALUE;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
int Map::size() const {
	return this->mapSize;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
bool Map::isEmpty() const{
	return this->mapSize == 0;
}

//BC: Theta(mapSize), WC: Theta(mapSize), TC: Theta(mapSize)
int Map::getValueRange() const {
    if(this->isEmpty())
        return -1;
    int minValue = this->elements[0].second;
    int maxValue = this->elements[0].second;
    for(int i = 1; i < this->mapSize; i++)
    {
        if(this->elements[i].second < minValue)
            minValue = this->elements[i].second;
        if(this->elements[i].second > maxValue)
            maxValue = this->elements[i].second;
    }
    return maxValue - minValue;
}

//BC: Theta(1), WC: Theta(1), TC: Theta(1)
MapIterator Map::iterator() const {
	return MapIterator(*this);
}



