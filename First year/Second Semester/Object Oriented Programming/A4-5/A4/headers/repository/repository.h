#pragma once
#include "../domain/dynamicVector.h"

template <typename type>
class Repository {
private:
    DynamicVector<type> elements;

public:
    Repository();
    Repository(const Repository &other);
    ~Repository();
    type &operator[](int index);

    void Add(type elem);
    void Remove(int index);
    int GetSize();
    DynamicVector<type> GetAll();
    bool Search(type elem) const;
};

template<typename type>
Repository<type>::Repository() {
    this->elements = DynamicVector<type>();
}

template<typename type>
Repository<type>::Repository(const Repository &other) {
    this->elements = other.elements;
}

template<typename type>
Repository<type>::~Repository() = default;

template<typename type>
type &Repository<type>::operator[](int index) {
    return this->elements[index];
}

template<typename type>
void Repository<type>::Add(type elem) {
    this->elements.AddToDynamicVector(elem);
}

template<typename type>
void Repository<type>::Remove(int index) {
    this->elements.RemoveFromDynamicVector(index);
}

template<typename type>
int Repository<type>::GetSize() {
    return this->elements.GetSizeOfDynamicVector();
}

template<typename type>
DynamicVector<type> Repository<type>::GetAll() {
    return this->elements;
}

template<typename type>
bool Repository<type>::Search(type elem) const {
    return this->elements.SearchInDynamicVector(elem);
}

