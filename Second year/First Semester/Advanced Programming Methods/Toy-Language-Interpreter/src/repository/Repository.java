package repository;

import model.state.PrgState;
import exceptions.InterpreterException;
import exceptions.RepositoryException;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Repository implements IRepository {
    private List<PrgState> prgStates;
    private String logFilePath;

    public Repository(PrgState initialState, String logFilePath) {
        prgStates = new ArrayList<>();
        prgStates.add(initialState);
        this.logFilePath = logFilePath;
    }

    @Override
    public List<PrgState> getPrgList() {
        return prgStates;
    }

    @Override
    public void setPrgList(List<PrgState> newList) {
        this.prgStates = newList;
    }

    @Override
    public void logPrgStateExec(PrgState prgState) throws InterpreterException {
        try (PrintWriter logFile = new PrintWriter(new BufferedWriter(new FileWriter(logFilePath, true)))) {
            logFile.print(prgState.toLogString());
        } catch (IOException e) {
            // If we previously threw MyException, now we throw a RepositoryException since it's a repository logging error
            throw new RepositoryException("Error writing to log file: " + e.getMessage());
        }
    }
}