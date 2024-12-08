package model.exp;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.values.IntValue;
import model.values.Value;
import model.types.IntType;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class ArithExp implements Exp {
    private Exp e1;
    private Exp e2;
    private int op; // 1 = +, 2 = -, 3 = *, 4 = /

    public ArithExp(int op, Exp e1, Exp e2) {
        this.op = op;
        this.e1 = e1;
        this.e2 = e2;
    }

    @Override
    public Value eval(MyIDictionary<String, Value> tbl) throws ExpressionException, ADTException {
        Value v1 = e1.eval(tbl);
        if (!v1.getType().equals(new IntType())) {
            throw new ExpressionException("First operand is not an integer");
        }
        Value v2 = e2.eval(tbl);
        if (!v2.getType().equals(new IntType())) {
            throw new ExpressionException("Second operand is not an integer");
        }

        IntValue i1 = (IntValue) v1;
        IntValue i2 = (IntValue) v2;
        int n1 = i1.getVal();
        int n2 = i2.getVal();

        switch (op) {
            case 1:
                return new IntValue(n1 + n2);
            case 2:
                return new IntValue(n1 - n2);
            case 3:
                return new IntValue(n1 * n2);
            case 4:
                if (n2 == 0) throw new ExpressionException("Division by zero");
                return new IntValue(n1 / n2);
            default:
                throw new ExpressionException("Invalid arithmetic operator");
        }
    }

    @Override
    public String toString() {
        return e1.toString() + " " + opToString() + " " + e2.toString();
    }

    private String opToString() {
        switch (op) {
            case 1:
                return "+";
            case 2:
                return "-";
            case 3:
                return "*";
            case 4:
                return "/";
            default:
                return "";
        }
    }
}