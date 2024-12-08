package model.stmt;

import model.state.PrgState;
import exceptions.StatementException;
import exceptions.InterpreterException;

public interface IStmt {
    PrgState execute(PrgState state) throws StatementException, InterpreterException;
}
