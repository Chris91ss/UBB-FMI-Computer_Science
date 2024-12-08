package model.datastructures;

import model.values.Value;
import exceptions.ADTException;

import java.util.Map;

public interface MyIHeap {
    int allocate(Value value);
    Value deallocate(int address) throws ADTException;
    Value get(int address) throws ADTException;
    boolean containsKey(int address);
    void update(int address, Value value) throws ADTException;
    Map<Integer, Value> getContent();
    void setContent(Map<Integer, Value> newContent);
    String toString();      // For displaying the heap
    String toLogString();   // For logging the heap content
}
