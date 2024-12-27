package model.exp;

import model.datastructures.MyIDictionary;
import model.datastructures.MyIHeap;
import model.types.RefType;
import model.types.Type;
import model.values.*;
import exceptions.ExpressionException;
import exceptions.ADTException;
import exceptions.DictionaryException;

public class ReadHeapExp implements Exp {
    private final Exp exp;

    public ReadHeapExp(Exp exp) {
        this.exp = exp;
    }

    @Override
    public Value eval(MyIDictionary<String, Value> symTable) throws ExpressionException, ADTException {
        Value val = exp.eval(symTable);
        if (!(val instanceof RefValue)) {
            throw new ExpressionException("ReadHeap error: The expression is not a RefValue.");
        }

        RefValue refVal = (RefValue) val;
        int address = refVal.getAddr();

        // Access the heap via the symbol table
        MyIHeap heap = symTable.getHeap();
        if (!heap.containsKey(address)) {
            throw new ExpressionException("ReadHeap error: Address " + address + " not found in the heap.");
        }

        return heap.get(address);
    }

    @Override
    public Type typecheck(MyIDictionary<String, Type> typeEnv) throws ExpressionException, DictionaryException {
        Type typ = exp.typecheck(typeEnv);
        if (typ instanceof RefType) {
            RefType reft = (RefType) typ;
            return reft.getInner();
        } else {
            throw new ExpressionException("The argument of rH is not a Ref Type");
        }
    }

    @Override
    public String toString() {
        return "rH(" + exp.toString() + ")";
    }
}
