package model.stmt;

import exceptions.ADTException;
import model.state.PrgState;
import model.exp.Exp;
import model.datastructures.MyIDictionary;
import model.values.Value;
import model.types.Type;
import exceptions.StatementException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class AssignStmt implements IStmt {
    private String id;
    private Exp exp;

    public AssignStmt(String id, Exp exp) {
        this.id = id;
        this.exp = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        MyIDictionary<String, Value> symTbl = state.getSymTable();
        try {
            Value val = exp.eval(symTbl);
            if (symTbl.isDefined(id)) {
                Type typeId = (symTbl.lookup(id)).getType();
                if (val.getType().equals(typeId)) {
                    symTbl.update(id, val);
                } else {
                    throw new StatementException("Declared type of variable '" + id + "' and type of the assigned expression do not match");
                }
            } else {
                throw new StatementException("The variable '" + id + "' was not declared before");
            }
        } catch (ExpressionException | ADTException e) {
            throw new StatementException(e.getMessage());
        }
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        Type varType = typeEnv.lookup(id);
        Type expType = exp.typecheck(typeEnv);
        if (varType.equals(expType)) {
            return typeEnv;
        } else {
            throw new StatementException("Declared type of variable '" + id + "' and type of the assigned expression do not match");
        }
    }

    @Override
    public String toString() {
        return id + " = " + exp.toString();
    }
}
