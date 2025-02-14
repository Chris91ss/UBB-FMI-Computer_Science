package model.state;

import exceptions.StackException;
import model.datastructures.*;
import model.stmt.IStmt;
import model.values.Value;
import model.values.StringValue;
import exceptions.InterpreterException;

import java.io.BufferedReader;
import java.util.concurrent.atomic.AtomicInteger;

public class PrgState {
    private final MyIStack<IStmt> exeStack;
    private final MyIDictionary<String, Value> symTable;
    private final MyIHeap heap;
    private final MyIList<Value> out;
    private final MyIDictionary<StringValue, BufferedReader> fileTable;

    private static AtomicInteger lastId = new AtomicInteger(0);
    private final int id;

    private static synchronized int getNewId() {
        return lastId.incrementAndGet();
    }

    public PrgState(MyIStack<IStmt> exeStack,
                    MyIDictionary<String, Value> symTable,
                    MyIHeap heap,
                    MyIList<Value> out,
                    MyIDictionary<StringValue, BufferedReader> fileTable,
                    IStmt originalProgram) {
        this.exeStack = exeStack;
        this.symTable = symTable;
        this.heap = heap;
        this.out = out;
        this.fileTable = fileTable;
        this.id = getNewId();
        if (originalProgram != null) {
            exeStack.push(originalProgram);
        }
    }

    public boolean isNotCompleted() {
        return !exeStack.isEmpty();
    }

    public PrgState oneStep() throws InterpreterException {
        if (exeStack.isEmpty())
            throw new StackException("prgstate stack is empty");
        IStmt crtStmt = exeStack.pop();
        return crtStmt.execute(this); // may return null or a new PrgState if fork
    }

    public MyIStack<IStmt> getStk() {return exeStack;}
    public MyIDictionary<String, Value> getSymTable() {return symTable;}
    public MyIHeap getHeap(){return heap;}
    public MyIList<Value> getOut(){return out;}
    public MyIDictionary<StringValue, BufferedReader> getFileTable(){return fileTable;}
    public int getId() { return id; }

    @Override
    public String toString() {
        return "Program ID: " + id + "\n" +
                "Execution Stack:\n" + exeStack.toString() + "\n" +
                "Symbol Table:\n" + symTable.toString() + "\n" +
                "Heap:\n" + heap.toString() + "\n" +
                "Output:\n" + out.toString() + "\n" +
                "File Table:\n" + fileTable.toString() + "\n";
    }

    public String toLogString() {
        return "Program ID: " + id + "\n" +
                "ExeStack:\n" + exeStack.toString() +
                "SymTable:\n" + symTable.toString() +
                "Heap:\n" + heap.toString() +
                "Out:\n" + out.toString() +
                "FileTable:\n" + fileTable.toString() + "\n";
    }
}
