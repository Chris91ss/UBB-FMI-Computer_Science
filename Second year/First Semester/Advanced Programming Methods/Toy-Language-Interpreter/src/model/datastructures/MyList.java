package model.datastructures;

import java.util.ArrayList;
import java.util.List;

public class MyList<T> implements MyIList<T> {
    private List<T> list;

    public MyList() {
        this.list = new ArrayList<>();
    }

    @Override
    public void add(T value) {
        list.add(value);
    }

    @Override
    public String toString() {
        return list.toString();
    }

    public String toLogString() {
        StringBuilder sb = new StringBuilder();
        for (T elem : list) {
            sb.append(elem.toString()).append("\n");
        }
        return sb.toString();
    }
}