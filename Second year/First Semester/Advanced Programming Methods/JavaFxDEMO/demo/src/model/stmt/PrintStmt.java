package model.stmt;

import exceptions.ADTException;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import model.exp.Exp;
import model.datastructures.MyIList;
import model.types.Type;
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
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException {
        try {
            exp.typecheck(typeEnv);
            return typeEnv;
        } catch (ExpressionException | DictionaryException e) {
            throw new StatementException(e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "Print(" + exp.toString() + ")";
    }
}
