#include "dynamicVector.h"

template <typename type>
class Repository {
private:
    DynamicVector<type> elements;

public:
    Repository();
    Repository(const Repository &other);
    ~Repository();
    type operator[](int index);

    void add(const type &element);
    DynamicVector<type> getAll() const;
    bool search(type element) const;
};

template<typename type>
Repository<type>::Repository() {
    elements = DynamicVector<type>();
}

template<typename type>
Repository<type>::Repository(const Repository &other) {
    elements = other.elements;
}

template<typename type>
Repository<type>::~Repository() = default;

template<typename type>
type Repository<type>::operator[](int index) {
    return this->elements[index];
}

template<typename type>
void Repository<type>::add(const type &element) {
    this->elements.AddToDynamicVector(element);
}

template<typename type>
DynamicVector<type> Repository<type>::getAll() const {
    return this->elements;
}

template<typename type>
bool Repository<type>::search(type element) const {
    return this->elements.SearchInDynamicVector(element);
}

