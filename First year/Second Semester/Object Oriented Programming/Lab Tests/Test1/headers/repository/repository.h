#pragma once
#include "dynamicVector.h"

template <typename type>
class Repository {
private:
        DynamicVector<type> elements;
public:
    Repository();
    Repository(const Repository<type> &other);
    ~Repository();
    type &operator[](int index);

    void addElementToRepository(type element);
    DynamicVector<type> getAllElementsFromRepository() const;
    int getSizeOfRepository() const;
    bool searchElementInRepository(type elem) const;
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
void Repository<type>::addElementToRepository(type element) {
    this->elements.AddToDynamicVector(element);
}

template<typename type>
DynamicVector<type> Repository<type>::getAllElementsFromRepository() const {
    return this->elements;
}

template<typename type>
int Repository<type>::getSizeOfRepository() const {
    return this->elements.GetSizeOfDynamicVector();
}

template<typename type>
bool Repository<type>::searchElementInRepository(type elem) const {
    return this->elements.SearchInDynamicVector(elem);
}
