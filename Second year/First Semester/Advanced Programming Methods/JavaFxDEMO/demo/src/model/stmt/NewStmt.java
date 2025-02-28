package model.stmt;

import model.exp.Exp;
import model.datastructures.*;
import model.state.PrgState;
import model.values.*;
import model.types.*;
import exceptions.StatementException;
import exceptions.ADTException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class NewStmt implements IStmt {
    private final String varName;
    private final Exp exp;

    public NewStmt(String varName, Exp exp) {
        this.varName = varName;
        this.exp = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException, ADTException, ExpressionException, DictionaryException {
        MyIDictionary<String, Value> symTable = state.getSymTable();
        MyIHeap heap = state.getHeap();

        if (!symTable.isDefined(varName)) {
            throw new StatementException("Variable " + varName + " is not defined.");
        }

        Value varValue = symTable.lookup(varName);
        if (!(varValue.getType() instanceof RefType)) {
            throw new StatementException("Variable " + varName + " is not of RefType.");
        }

        RefType refType = (RefType) varValue.getType();
        Type locationType = refType.getInner();

        Value expValue = exp.eval(symTable);
        if (!expValue.getType().equals(locationType)) {
            throw new StatementException("Type of the expression and the locationType do not match.");
        }

        int address = heap.allocate(expValue);
        symTable.update(varName, new RefValue(address, locationType));

        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        Type varType = typeEnv.lookup(varName);
        Type expType = exp.typecheck(typeEnv);

        if (varType.equals(new RefType(expType))) {
            return typeEnv;
        } else {
            throw new StatementException("Declared type of variable '" + varName + "' and type of the assigned expression do not match");
        }
    }

    @Override
    public String toString() {
        return "new(" + varName + ", " + exp.toString() + ")";
    }
}
