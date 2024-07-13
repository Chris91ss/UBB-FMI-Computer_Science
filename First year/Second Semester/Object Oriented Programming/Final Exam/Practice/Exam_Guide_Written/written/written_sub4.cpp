#include <iostream>

class Person
{
public:
    Person() { std::cout << "Person{}"; }
    virtual void print() = 0;
    virtual ~Person() { std::cout << "~Person()"; }
};

class Student : public Person
{
public:
    Student() { std::cout << "Student{}";
    }
    void print() override { std::cout << "Student"; }
    virtual ~Student() { std::cout << "~Student()"; }
};

// int main()
// {
//     //Person* p = new Person{}; // error: cannot declare variable ‘p’ to be of abstract type ‘Person’,
//     //because we have a purely virtual function print() => Person is an abstract class
//     //delete p;
//     Person* s = new Student{};
//     s->print();
//     delete s;
//     return 0;
// }