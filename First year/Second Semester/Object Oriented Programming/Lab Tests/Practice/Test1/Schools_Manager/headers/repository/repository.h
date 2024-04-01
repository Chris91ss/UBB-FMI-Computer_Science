#include "dynamicVector.h"
#pragma once

template <typename type>
class Repository {
private:
    DynamicVector<type> elements;
public:
    Repository();
    Repository(const Repository<type> &other);
    ~Repository();
    type &operator[](int index);

    void addElement(const type &element);
    void removeElement(int index);
    DynamicVector<type> getAllElements() const;
    int getSize() const;
    bool searchElement(type elem) const;
};

template<typename type>
Repository<type>::Repository() {
    this->elements = DynamicVector<type>();
}

template<typename type>
Repository<type>::Repository(const Repository<type> &other) {
    this->elements = other.elements;
}

template<typename type>
Repository<type>::~Repository() = default;

template<typename type>
type &Repository<type>::operator[](int index) {
    return this->elements[index];
}

template<typename type>
void Repository<type>::addElement(const type &element) {
    this->elements.AddToDynamicVector(element);
}

template<typename type>
void Repository<type>::removeElement(const int index) {
    this->elements.RemoveFromDynamicVector(index);
}

template<typename type>
DynamicVector<type> Repository<type>::getAllElements() const {
    return this->elements;
}

template<typename type>
int Repository<type>::getSize() const {
    return this->elements.GetSizeOfDynamicVector();
}

template<typename type>
bool Repository<type>::searchElement(type elem) const {
    return this->elements.SearchInDynamicVector(elem);
}
