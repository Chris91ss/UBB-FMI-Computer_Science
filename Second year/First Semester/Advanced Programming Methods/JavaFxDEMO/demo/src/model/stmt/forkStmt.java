package model.stmt;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import exceptions.StatementException;
import model.datastructures.*;
import model.state.PrgState;
import model.types.Type;
import model.values.Value;
import exceptions.InterpreterException;

public class forkStmt implements IStmt {
    private IStmt stmt;

    public forkStmt(IStmt stmt) {
        this.stmt = stmt;
    }

    @Override
    public PrgState execute(PrgState state) throws InterpreterException {
        MyIDictionary<String, Value> newSymTable = state.getSymTable().deepCopy();
        // Same heap, out, fileTable references
        MyIHeap heap = state.getHeap();
        MyIList<Value> out = state.getOut();
        MyIDictionary<model.values.StringValue, java.io.BufferedReader> fileTable = state.getFileTable();

        MyIStack<IStmt> newStack = new MyStack<>();
        newStack.push(stmt);

        PrgState newPrg = new PrgState(newStack, newSymTable, heap, out, fileTable, null);
        return newPrg;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        stmt.typecheck(typeEnv);
        return typeEnv;
    }

    @Override
    public String toString() {
        return "fork(" + stmt.toString() + ")";
    }
}
