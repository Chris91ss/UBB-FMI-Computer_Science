package model.exp;

import model.datastructures.MyIDictionary;
import model.values.Value;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class VarExp implements Exp {
    private String id;

    public VarExp(String id) {
        this.id = id;
    }

    @Override
    public Value eval(MyIDictionary<String, Value> tbl) throws ExpressionException, DictionaryException {
        return tbl.lookup(id);
    }

    @Override
    public String toString() {
        return id;
    }
}
