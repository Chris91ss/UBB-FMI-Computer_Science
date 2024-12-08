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
    public PrgState getCrtPrg() throws RepositoryException {
        if (prgStates.isEmpty()) {
            throw new RepositoryException("Repository is empty");
        }
        return prgStates.get(0);
    }

    @Override
    public void logPrgStateExec() throws InterpreterException {
        PrgState prgState = getCrtPrg();
        try (PrintWriter logFile = new PrintWriter(new BufferedWriter(new FileWriter(logFilePath, true)))) {
            logFile.println(prgState.toLogString());
            logFile.flush();
        } catch (IOException e) {
            throw new RepositoryException("Error writing to log file: " + e.getMessage());
        }
    }
}