// File: src/model/state/PrgState.java
package model.state;

import model.datastructures.*;
import model.stmt.IStmt;
import model.values.Value;
import model.values.StringValue;
import exceptions.InterpreterException;

import java.io.BufferedReader;

public class PrgState {
    private final MyIStack<IStmt> exeStack;
    private final MyIDictionary<String, Value> symTable;
    private final MyIHeap heap;
    private final MyIList<Value> out;
    private final MyIDictionary<StringValue, BufferedReader> fileTable;

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
        this.exeStack.push(originalProgram);
    }

    public MyIStack<IStmt> getStk() {
        return exeStack;
    }

    public MyIDictionary<String, Value> getSymTable() {
        return symTable;
    }

    public MyIHeap getHeap() {
        return heap;
    }

    public MyIList<Value> getOut() {
        return out;
    }

    public MyIDictionary<StringValue, BufferedReader> getFileTable() {
        return fileTable;
    }

    @Override
    public String toString() {
        return "Execution Stack:\n" + exeStack.toString() + "\n" +
                "Symbol Table:\n" + symTable.toString() + "\n" +
                "Heap:\n" + heap.toString() + "\n" +
                "Output:\n" + out.toString() + "\n" +
                "File Table:\n" + fileTable.toString() + "\n";
    }

    public String toLogString() {
        StringBuilder sb = new StringBuilder();
        sb.append("ExeStack:\n");
        sb.append(exeStack.toLogString());
        sb.append("SymTable:\n");
        sb.append(symTable.toLogString());
        sb.append("Heap:\n");
        sb.append(heap.toLogString());
        sb.append("Out:\n");
        sb.append(out.toLogString());
        sb.append("FileTable:\n");
        sb.append(fileTable.toLogString());
        sb.append("\n");
        return sb.toString();
    }
}
