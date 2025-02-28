package model.datastructures;

import java.util.List;

public interface MyIList<T> {
    void add(T value);
    List<T> getList();
    String toString();
    String toLogString();
}