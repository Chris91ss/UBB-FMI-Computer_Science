package model.exp;

import model.datastructures.MyIDictionary;
import model.values.Value;

public class ValueExp implements Exp {
    private Value value;

    public ValueExp(Value value) {
        this.value = value;
    }

    @Override
    public Value eval(MyIDictionary<String, Value> tbl) {
        return value;
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
