package controller;

import model.state.PrgState;
import repository.IRepository;
import exceptions.InterpreterException;
import exceptions.ControllerException;
import exceptions.StackException;
import exceptions.ADTException;
import model.values.Value;
import model.values.RefValue;

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class Controller {
    private IRepository repo;
    private boolean displayFlag;
    private ExecutorService executor; // new field

    public Controller(IRepository repo) {
        this.repo = repo;
        this.displayFlag = false;
    }

    public void setDisplayFlag(boolean flag) {
        this.displayFlag = flag;
    }

    public IRepository getRepo() {
        return this.repo;
    }

    List<PrgState> removeCompletedPrg(List<PrgState> inPrgList) {
        return inPrgList.stream()
                .filter(PrgState::isNotCompleted)
                .collect(Collectors.toList());
    }

    private void oneStepForAllPrg(List<PrgState> prgList) throws InterpreterException {
        // Before the execution, print the PrgState List into the log file
        prgList.forEach(prg -> {
            try {
                repo.logPrgStateExec(prg);
            } catch (InterpreterException e) {
                System.out.println("Error logging state: " + e.getMessage());
            }
        });

        // Display states if displayFlag is true
        if (displayFlag) {
            System.out.println("Current Program States before execution of oneStep:");
            prgList.forEach(prg -> System.out.println(prg.toString()));
        }

        // RUN concurrently one step for each of the existing PrgStates
        List<Callable<PrgState>> callList = prgList.stream()
                .map((PrgState p) -> (Callable<PrgState>) (p::oneStep))
                .collect(Collectors.toList());

        List<PrgState> newPrgList;
        try {
            newPrgList = executor.invokeAll(callList).stream()
                    .map(future -> {
                        try {
                            return future.get();
                        } catch (ExecutionException | InterruptedException e) {
                            System.out.println("Error in threads: " + e.getMessage());
                            return null;
                        }
                    })
                    .filter(p -> p != null)
                    .collect(Collectors.toList());
        } catch (InterruptedException e) {
            throw new InterpreterException("Thread execution interrupted: " + e.getMessage());
        }

        // Add the new created threads to the list of existing threads
        prgList.addAll(newPrgList);

        // After the execution, print the PrgState List into the log file
        prgList.forEach(prg -> {
            try {
                repo.logPrgStateExec(prg);
            } catch (InterpreterException e) {
                System.out.println("Error logging state: " + e.getMessage());
            }
        });

        // Display states if displayFlag is true
        if (displayFlag) {
            System.out.println("Current Program States after execution of oneStep:");
            prgList.forEach(prg -> System.out.println(prg.toString()));
        }

        // Save the current programs in the repository
        repo.setPrgList(prgList);
    }

    public void allStep() throws InterpreterException {
        executor = Executors.newFixedThreadPool(2);

        List<PrgState> prgList = removeCompletedPrg(repo.getPrgList());
        List<PrgState> lastKnownStates = null; // Backup for final states

        while (prgList.size() > 0) {
            lastKnownStates = new ArrayList<>(prgList); // Backup current states

            conservativeGarbageCollector(prgList);
            oneStepForAllPrg(prgList);

            // After executing one step for all prg, we remove completed again
            prgList = removeCompletedPrg(repo.getPrgList());
        }

        executor.shutdownNow();
        repo.setPrgList(prgList);

        // If we end up with no states and displayFlag = no, print the last known states
        // because no states have been printed during execution
        if ((lastKnownStates != null) && (lastKnownStates.size() > 0) && !displayFlag) {
            System.out.println("Final Program States:");
            for (PrgState state : lastKnownStates) {
                System.out.println(state.toString());
            }
        }
    }


    private void conservativeGarbageCollector(List<PrgState> prgList) throws InterpreterException {
        List<Integer> symTableAddrs = prgList.stream()
                .flatMap(p -> getAddrFromSymTable(p.getSymTable().values()).stream())
                .collect(Collectors.toList());

        PrgState anyPrg = prgList.get(0);
        Map<Integer,Value> heap = anyPrg.getHeap().getContent();
        Map<Integer,Value> newHeap = safeGarbageCollector(symTableAddrs, heap);
        anyPrg.getHeap().setContent(newHeap);
    }

    private List<Integer> getAddrFromSymTable(Collection<Value> symTableValues) {
        return symTableValues.stream()
                .filter(v -> v instanceof RefValue)
                .map(v -> ((RefValue)v).getAddr())
                .collect(Collectors.toList());
    }

    private Map<Integer,Value> safeGarbageCollector(List<Integer> symTableAddr, Map<Integer,Value> heap) {
        return heap.entrySet().stream()
                .filter(e -> symTableAddr.contains(e.getKey()))
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }
}
