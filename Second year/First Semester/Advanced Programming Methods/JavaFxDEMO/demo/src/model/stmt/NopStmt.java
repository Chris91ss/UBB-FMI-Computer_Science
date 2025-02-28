package model.stmt;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import exceptions.StatementException;
import model.types.Type;

public class NopStmt implements IStmt {
    @Override
    public PrgState execute(PrgState state) {
        // Does nothing
        return null;
    }

    @Override
    public MyIDictionary<String, Type> typecheck(MyIDictionary<String, Type> typeEnv) throws StatementException, ExpressionException, DictionaryException {
        return typeEnv;
    }

    @Override
    public String toString() {
        return "nop";
    }
}
