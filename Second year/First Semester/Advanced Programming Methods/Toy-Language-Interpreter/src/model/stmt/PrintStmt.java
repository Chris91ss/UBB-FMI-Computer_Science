package model.stmt;

import exceptions.ADTException;
import model.state.PrgState;
import model.exp.Exp;
import model.datastructures.MyIList;
import model.values.Value;
import exceptions.StatementException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;

public class PrintStmt implements IStmt {
    private Exp exp;

    public PrintStmt(Exp exp) {
        this.exp = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws StatementException {
        try {
            MyIList<Value> out = state.getOut();
            Value val = exp.eval(state.getSymTable());
            out.add(val);
        } catch (ExpressionException | ADTException e) {
            throw new StatementException(e.getMessage());
        }
        return null;
    }

    @Override
    public String toString() {
        return "Print(" + exp.toString() + ")";
    }
}
