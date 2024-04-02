#pragma once
#include <stdexcept>
using namespace std;

template <typename type>
class DynamicVector {
private:
    int length{};
    int capacity{};
    type *elements;

    void resize(double resizeFactor = 2);

public:
    DynamicVector();
    DynamicVector(const DynamicVector<type> &other);
    ~DynamicVector();
    DynamicVector<type> &operator=(const DynamicVector<type> &other);
    type &operator[](int index) const;

    void AddToDynamicVector(type elem);
    void RemoveFromDynamicVector(int index);
    int GetSizeOfDynamicVector() const;
    bool SearchInDynamicVector(type elem) const;
};

template<typename type>
type &DynamicVector<type>::operator[](int index) const {
    if (index < 0 || index >= this->length)
        throw runtime_error("index out of range");
    return this->elements[index];
}

template<typename type>
void DynamicVector<type>::resize(double resizeFactor) {
    this->capacity *= resizeFactor;
    type *newElements = new type[this->capacity];
    for (int i = 0; i < this->length; i++)
        newElements[i] = this->elements[i];
    delete[] this->elements;
    this->elements = newElements;
}

template<typename type>
DynamicVector<type>::DynamicVector() {
    this->length = 0;
    this->capacity = 2;
    this->elements = new type[this->capacity];
}

template<typename type>
DynamicVector<type>::DynamicVector(const DynamicVector<type> &other) {
    this->length = other.length;
    this->capacity = other.capacity;
    this->elements = new type[this->capacity];
    for (int i = 0; i < this->length; i++)
        this->elements[i] = other.elements[i];
}

template<typename type>
DynamicVector<type>::~DynamicVector() {
    delete[] this->elements;
}

template<typename type>
DynamicVector<type> &DynamicVector<type>::operator=(const DynamicVector<type> &other) {
    if (this == &other)
        return *this;

    this->length = other.length;
    this->capacity = other.capacity;
    delete[] this->elements;
    this->elements = new type[this->capacity];
    for (int i = 0; i < this->length; i++)
        this->elements[i] = other.elements[i];
    return *this;
}

template<typename type>
void DynamicVector<type>::AddToDynamicVector(type elem) {
    if (this->length == this->capacity)
        this->resize();
    this->elements[this->length++] = elem;
}

template<typename type>
void DynamicVector<type>::RemoveFromDynamicVector(int index) {
    if (index < 0 || index >= this->length)
        throw runtime_error("index out of range");

    for (int i = index; i < this->length - 1; i++)
        this->elements[i] = this->elements[i + 1];
    this->length--;

    if (this->length == int(this->capacity / 4) && this->capacity > 2)
        this->resize(0.5);
}

template<typename type>
int DynamicVector<type>::GetSizeOfDynamicVector() const {
    return this->length;
}

template<typename type>
bool DynamicVector<type>::SearchInDynamicVector(type elem) const {
    for (int i = 0; i < this->length; i++)
        if (this->elements[i] == elem)
            return true;
    return false;
}



