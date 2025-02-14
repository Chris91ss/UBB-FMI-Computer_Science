package model.exp;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.types.Type;
import model.values.Value;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public interface Exp {
    Value eval(MyIDictionary<String, Value> tbl) throws ExpressionException, DictionaryException, ADTException;
    Type typecheck(MyIDictionary<String, Type> typeEnv) throws ExpressionException, DictionaryException;
}