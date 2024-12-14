package repository;

import model.state.PrgState;
import exceptions.InterpreterException;

import java.util.List;

public interface IRepository {
    void logPrgStateExec(PrgState prgState) throws InterpreterException;
    List<PrgState> getPrgList();
    void setPrgList(List<PrgState> newList);
}