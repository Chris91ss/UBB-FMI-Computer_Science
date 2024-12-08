package model.exp;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.values.BoolValue;
import model.values.Value;
import model.types.BoolType;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class LogicExp implements Exp {
    private Exp e1;
    private Exp e2;
    private String op; // "and" or "or"

    public LogicExp(String op, Exp e1, Exp e2) {
        this.op = op;
        this.e1 = e1;
        this.e2 = e2;
    }

    @Override
    public Value eval(MyIDictionary<String, Value> tbl) throws ExpressionException, ADTException {
        Value v1 = e1.eval(tbl);

        if (!v1.getType().equals(new BoolType())) {
            throw new ExpressionException("First operand is not a boolean");
        }

        Value v2 = e2.eval(tbl);

        if (!v2.getType().equals(new BoolType())) {
            throw new ExpressionException("Second operand is not a boolean");
        }

        BoolValue b1 = (BoolValue) v1;
        BoolValue b2 = (BoolValue) v2;

        boolean n1 = b1.getVal();
        boolean n2 = b2.getVal();

        if (op.equals("and")) {
            return new BoolValue(n1 && n2);
        } else if (op.equals("or")) {
            return new BoolValue(n1 || n2);
        } else {
            throw new ExpressionException("Invalid logical operator");
        }
    }

    @Override
    public String toString() {
        return e1.toString() + " " + op + " " + e2.toString();
    }
}
