package model.datastructures;

import exceptions.StackException;

import java.util.Stack;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.stream.Collectors;

public class MyStack<T> implements MyIStack<T> {
    private Stack<T> stack;

    public MyStack() {
        this.stack = new Stack<>();
    }

    @Override
    public T pop() throws StackException {
        if (stack.isEmpty()) {
            throw new StackException("Cannot pop from an empty stack.");
        }
        return stack.pop();
    }

    @Override
    public void push(T v) {
        stack.push(v);
    }

    @Override
    public boolean isEmpty() {
        return stack.isEmpty();
    }

    public Stack<T> getStack() {
        return stack; // return the internal java.util.Stack
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        List<T> elements = new ArrayList<>(stack);
        Collections.reverse(elements); // Display top of stack first
        sb.append(elements.stream().map(Object::toString).collect(Collectors.joining(", ")));
        sb.append("]");
        return sb.toString();
    }

    public String toLogString() {
        StringBuilder sb = new StringBuilder();
        List<T> elements = new ArrayList<>(stack);
        Collections.reverse(elements); // To display the top of the stack first
        for (T elem : elements) {
            sb.append(elem.toString()).append("\n");
        }
        return sb.toString();
    }
}