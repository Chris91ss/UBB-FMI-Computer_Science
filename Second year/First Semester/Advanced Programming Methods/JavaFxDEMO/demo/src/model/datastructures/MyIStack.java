package model.datastructures;
import exceptions.StackException;
import java.util.Stack;

public interface MyIStack<T> {
    T pop() throws StackException;
    void push(T v);
    boolean isEmpty();
    Stack<T> getStack();
    String toString();
    String toLogString();
}