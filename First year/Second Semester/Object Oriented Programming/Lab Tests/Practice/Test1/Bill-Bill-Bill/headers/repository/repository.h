#pragma once
#include "dynamicVector.h"

template <typename type>
class Repository {
private:
    DynamicVector<type> elements;
public:
    Repository();
    Repository(const Repository<type>& repository);
    ~Repository();
    type operator[](int index);

    void addElement(type element);
    void removeElement(int index);
    bool searchElement(type element);
    DynamicVector<type> getAll() const;
    int getSize() const;
};

template<typename type>
Repository<type>::Repository() {
    this->elements = DynamicVector<type>();
}

template<typename type>
Repository<type>::Repository(const Repository<type> &repository) {
    this->elements = repository.elements;
}

template<typename type>
Repository<type>::~Repository() = default;

template<typename type>
type Repository<type>::operator[](int index) {
    return this->elements[index];
}

template<typename type>
void Repository<type>::addElement(type element) {
    this->elements.AddToDynamicVector(element);
}

template<typename type>
void Repository<type>::removeElement(int index) {
    this->elements.RemoveFromDynamicVector(index);
}

template<typename type>
bool Repository<type>::searchElement(type element) {
    return this->elements.SearchInDynamicVector(element);
}

template<typename type>
DynamicVector<type> Repository<type>::getAll() const {
    return this->elements;
}

template<typename type>
int Repository<type>::getSize() const {
    return this->elements.GetSizeOfDynamicVector();
}