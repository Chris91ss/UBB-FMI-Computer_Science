package model.stmt;

import model.datastructures.*;
import model.exp.Exp;
import model.state.PrgState;
import model.values.*;
import model.types.Type;
import exceptions.StatementException;
import exceptions.ADTException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class WriteHeapStmt implements IStmt {
    private final String varName;
    private final Exp exp;

    public WriteHeapStmt(String varName, Exp exp) {
        this.varName = varName;
        this.exp = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException, ADTException, ExpressionException, DictionaryException {
        MyIDictionary<String, Value> symTable = state.getSymTable();
        MyIHeap heap = state.getHeap();

        if (!symTable.isDefined(varName)) {
            throw new StatementException("WriteHeap error: Variable " + varName + " is not defined.");
        }

        Value varValue = symTable.lookup(varName);
        if (!(varValue instanceof RefValue)) {
            throw new StatementException("WriteHeap error: Variable " + varName + " is not a RefValue.");
        }

        RefValue refVal = (RefValue) varValue;
        int address = refVal.getAddr();

        if (!heap.containsKey(address)) {
            throw new StatementException("WriteHeap error: Address " + address + " not found in the heap.");
        }

        Value expValue = exp.eval(symTable);
        Type locationType = refVal.getLocationType();

        if (!expValue.getType().equals(locationType)) {
            throw new StatementException("WriteHeap error: Type mismatch between variable and expression.");
        }

        heap.update(address, expValue);
        return null;
    }

    @Override
    public String toString() {
        return "wH(" + varName + ", " + exp.toString() + ")";
    }
}