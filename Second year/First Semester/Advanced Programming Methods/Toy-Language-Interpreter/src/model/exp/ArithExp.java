package model.exp;

import exceptions.ADTException;
import exceptions.DictionaryException;
import exceptions.ExpressionException;
import model.datastructures.MyIDictionary;
import model.types.IntType;
import model.types.Type;
import model.values.IntValue;
import model.values.Value;

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
        // Evaluate the first operand
        Value v1 = e1.eval(tbl);
        if (!v1.getType().equals(new IntType())) {
            throw new ExpressionException("First operand is not an integer");
        }

        // Evaluate the second operand
        Value v2 = e2.eval(tbl);
        if (!v2.getType().equals(new IntType())) {
            throw new ExpressionException("Second operand is not an integer");
        }

        // Retrieve integer values
        int n1 = ((IntValue) v1).getVal();
        int n2 = ((IntValue) v2).getVal();

        // Perform the arithmetic operation based on the operator
        switch (op) {
            case 1: // Addition
                return new IntValue(n1 + n2);
            case 2: // Subtraction
                return new IntValue(n1 - n2);
            case 3: // Multiplication
                return new IntValue(n1 * n2);
            case 4: // Division
                if (n2 == 0) {
                    throw new ExpressionException("Division by zero");
                }
                return new IntValue(n1 / n2);
            default:
                throw new ExpressionException("Invalid arithmetic operator: " + op);
        }
    }

    @Override
    public Type typecheck(MyIDictionary<String, Type> typeEnv) throws ExpressionException, DictionaryException {
        // Type check the first operand
        Type t1 = e1.typecheck(typeEnv);
        if (!t1.equals(new IntType())) {
            throw new ExpressionException("First operand is not an integer");
        }

        // Type check the second operand
        Type t2 = e2.typecheck(typeEnv);
        if (!t2.equals(new IntType())) {
            throw new ExpressionException("Second operand is not an integer");
        }

        // Validate the operator
        if (op < 1 || op > 4) {
            throw new ExpressionException("Invalid arithmetic operator: " + op);
        }

        // The result of any arithmetic operation is an integer
        return new IntType();
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
                return "?"; // Represents an unknown operator
        }
    }
}
