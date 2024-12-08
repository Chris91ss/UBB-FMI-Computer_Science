package model.datastructures;

import exceptions.StackException;

public interface MyIStack<T> {
    T pop() throws StackException;
    void push(T v);
    boolean isEmpty();
    String toString();
    String toLogString();
}