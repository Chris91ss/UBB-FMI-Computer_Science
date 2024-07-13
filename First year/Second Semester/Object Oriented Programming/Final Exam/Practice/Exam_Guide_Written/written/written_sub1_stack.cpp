#include "written_sub1_stack.h"
#include <iostream>

void testStack()
{
    Stack<std::string> s{ 2 };
    assert(s.getMaxCapacity() == 2);
    try {
        s = s + "examination";
        s = s + "oop";
        s = s + "test";
    }
    catch (std::exception& e) {
        assert(strcmp(e.what(), "Stack is full!") == 0);
    }
    assert(s.pop() == "oop");
    assert(s.pop() == "examination");
}

// int main()
// {
//     testStack();
//     cout << "All tests passed!" << endl;
//     return 0;
// }