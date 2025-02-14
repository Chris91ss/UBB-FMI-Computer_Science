package model.values;

import model.types.BoolType;
import model.types.Type;

public class BoolValue implements Value {
    boolean val;

    public BoolValue(boolean val) {
        this.val = val;
    }

    public boolean getVal() {
        return val;
    }

    @Override
    public Type getType() {
        return new BoolType();
    }

    @Override
    public String toString() {
        return Boolean.toString(val);
    }
}
