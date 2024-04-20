#pragma once
#include<vector>
#include<utility>
//DO NOT INCLUDE MultiMapIterator

using namespace std;

//DO NOT CHANGE THIS PART
typedef int TKey;
typedef int TValue;
typedef std::pair<TKey, TValue> TElem;
typedef bool (*Condition)(TKey);
#define NULL_TVALUE -111111
#define NULL_TELEM pair<int,int>(-111111, -111111)
class MultiMapIterator;

// Structure for a node in the doubly linked list
struct DLLNode {
    TElem info;
    DLLNode* next;
    DLLNode* prev;

    DLLNode(const TElem& element, DLLNode* prevNode = nullptr, DLLNode* nextNode = nullptr)
            : info(element), prev(prevNode), next(nextNode) {}
};

// Structure for the doubly linked list itself
struct DLL {
    DLLNode* head;
    DLLNode* tail;

    DLL() : head(nullptr), tail(nullptr) {}
};

class MultiMap
{
	friend class MultiMapIterator;

private:
    DLL list;
    int length;

public:
	//constructor
	MultiMap();

	//adds a key value pair to the multimap
	void add(TKey c, TValue v);

	//removes a key value pair from the multimap
	//returns true if the pair was removed (if it was in the multimap) and false otherwise
	bool remove(TKey c, TValue v);

	//returns the vector of values associated to a key. If the key is not in the MultiMap, the vector is empty
	vector<TValue> search(TKey c) const;

	//returns the number of pairs from the multimap
	int size() const;

	//checks whether the multimap is empty
	bool isEmpty() const;

    //keeps in the MultiMap only those pairs whose key respects the given condition
    void filter(bool (*condition)(TKey));

	//returns an iterator for the multimap
	MultiMapIterator iterator() const;

	//descturctor
	~MultiMap();


};

