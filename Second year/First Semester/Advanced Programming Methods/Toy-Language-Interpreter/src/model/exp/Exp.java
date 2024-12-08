package model.exp;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.values.Value;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public interface Exp {
    Value eval(MyIDictionary<String, Value> tbl) throws ExpressionException, DictionaryException, ADTException;
}