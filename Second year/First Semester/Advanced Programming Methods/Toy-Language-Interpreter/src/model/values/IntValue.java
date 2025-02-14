package model.values;

import model.types.IntType;
import model.types.Type;

public class IntValue implements Value {
    int val;

    public IntValue(int val) {
        this.val = val;
    }

    public int getVal() {
        return val;
    }

    @Override
    public Type getType() {
        return new IntType();
    }

    @Override
    public String toString() {
        return Integer.toString(val);
    }
}
