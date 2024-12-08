package model.stmt;

import model.state.PrgState;
import exceptions.StatementException;

public class NopStmt implements IStmt {
    @Override
    public PrgState execute(PrgState state) {
        // Does nothing
        return state;
    }

    @Override
    public String toString() {
        return "nop";
    }
}
