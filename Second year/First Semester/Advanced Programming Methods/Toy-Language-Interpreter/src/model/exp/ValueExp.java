package model.exp;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import model.datastructures.MyIDictionary;
import model.types.Type;
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
    public Type typecheck(MyIDictionary<String, Type> typeEnv) throws ExpressionException, DictionaryException {
        return value.getType();
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
