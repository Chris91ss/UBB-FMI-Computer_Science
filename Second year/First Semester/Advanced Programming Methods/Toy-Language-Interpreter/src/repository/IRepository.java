package repository;

import model.state.PrgState;
import exceptions.InterpreterException;

public interface IRepository {
    PrgState getCrtPrg() throws InterpreterException;
    void logPrgStateExec() throws InterpreterException;
}