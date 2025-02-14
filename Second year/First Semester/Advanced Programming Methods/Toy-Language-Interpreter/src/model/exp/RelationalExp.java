package model.exp;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.types.IntType;
import model.types.Type;
import model.values.IntValue;
import model.values.Value;
import model.values.BoolValue;
import model.types.BoolType;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class RelationalExp implements Exp {
    private Exp e1;
    private Exp e2;
    private String op; // "<", "<=", "==", "!=", ">", ">="

    public RelationalExp(String op, Exp e1, Exp e2) {
        this.e1 = e1;
        this.e2 = e2;
        this.op = op;
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

        int n1 = ((IntValue) v1).getVal();
        int n2 = ((IntValue) v2).getVal();

        boolean result;
        switch (op) {
            case "<":
                result = n1 < n2;
                break;
            case "<=":
                result = n1 <= n2;
                break;
            case "==":
                result = n1 == n2;
                break;
            case "!=":
                result = n1 != n2;
                break;
            case ">":
                result = n1 > n2;
                break;
            case ">=":
                result = n1 >= n2;
                break;
            default:
                throw new ExpressionException("Invalid relational operator");
        }
        return new BoolValue(result);
    }

    @Override
    public Type typecheck(MyIDictionary<String, Type> typeEnv) throws ExpressionException, DictionaryException {
        Type typ1, typ2;
        typ1 = e1.typecheck(typeEnv);
        typ2 = e2.typecheck(typeEnv);
        if (!typ1.equals(new IntType()))
            throw new ExpressionException("First operand is not an integer");
        if (!typ2.equals(new IntType()))
            throw new ExpressionException("Second operand is not an integer");
        if(!op.equals("<") && !op.equals("<=") && !op.equals("==") && !op.equals("!=") && !op.equals(">") && !op.equals(">="))
            throw new ExpressionException("Invalid relational operator");
        return new BoolType();
    }

    @Override
    public String toString() {
        return e1.toString() + " " + op + " " + e2.toString();
    }
}