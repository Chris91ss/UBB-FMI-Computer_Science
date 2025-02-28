package controller;

import exceptions.InterpreterException;
import model.state.PrgState;
import model.values.RefValue;
import model.values.Value;
import repository.IRepository;

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

/**
 * Controller that manages the execution of Program States, with single-step & entire-run methods.
 */
public class Controller {
    private IRepository repo;
    private boolean displayFlag;
    private ExecutorService executor; // for concurrent execution

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

    /**
     * Single-step for the GUI.
     * If all states are done, we skip or throw an error.
     */
    public void oneStepGUI() throws InterpreterException {
        // create or reuse the executor
        if (executor == null || executor.isShutdown()) {
            executor = Executors.newFixedThreadPool(2);
        }

        // remove completed states
        List<PrgState> prgList = removeCompletedPrg(repo.getPrgList());
        if (prgList.isEmpty()) {
            throw new InterpreterException("No more states to execute!");
        }

        // 1) GC
        conservativeGarbageCollector(prgList);

        // 2) one step
        oneStepForAllPrg(prgList);

        // 3) remove completed again
        prgList = removeCompletedPrg(repo.getPrgList());
        repo.setPrgList(prgList);

        // if none left, shut down
        if (prgList.isEmpty()) {
            executor.shutdownNow();
        }
    }

    /**
     * Runs the entire program until no states remain.
     * Then sets the final snapshot in the repository so the GUI can show it.
     */
    public void allStep() throws InterpreterException {
        executor = Executors.newFixedThreadPool(2);
        List<PrgState> prgList = removeCompletedPrg(repo.getPrgList());
        List<PrgState> lastKnownNonEmptyStates = new ArrayList<>(prgList);

        while (!prgList.isEmpty()) {
            lastKnownNonEmptyStates = new ArrayList<>(prgList);
            conservativeGarbageCollector(prgList);
            oneStepForAllPrg(prgList);
            prgList = removeCompletedPrg(repo.getPrgList());
        }

        // final snapshot
        repo.setPrgList(lastKnownNonEmptyStates);
        executor.shutdownNow();

        if (!displayFlag) {
            System.out.println("Final Program States:");
            for (PrgState st : lastKnownNonEmptyStates) {
                System.out.println(st);
            }
        }
    }


    /**
     * Removes finished programs (those with an empty exeStack).
     */
    public List<PrgState> removeCompletedPrg(List<PrgState> inPrgList) {
        return inPrgList.stream()
                .filter(PrgState::isNotCompleted)
                .collect(Collectors.toList());
    }

    /**
     * Perform one step for each ProgramState concurrently.
     */
    private void oneStepForAllPrg(List<PrgState> prgList) throws InterpreterException {
        // Print or log states before stepping
        for (PrgState prg : prgList) {
            try {
                repo.logPrgStateExec(prg);
            } catch (InterpreterException e) {
                System.out.println("Error logging state: " + e.getMessage());
            }
        }

        if (displayFlag) {
            System.out.println("Current Program States before oneStep:");
            prgList.forEach(prg -> System.out.println(prg));
        }

        // build callables
        List<Callable<PrgState>> callList = prgList.stream()
                .map((PrgState p) -> (Callable<PrgState>)(p::oneStep))
                .collect(Collectors.toList());

        // run them
        List<PrgState> newPrgList;
        try {
            newPrgList = executor.invokeAll(callList).stream()
                    .map(future -> {
                        try {
                            return future.get();
                        } catch (InterruptedException | ExecutionException e) {
                            System.out.println("Error in threads: " + e.getMessage());
                            return null;
                        }
                    })
                    .filter(Objects::nonNull)
                    .collect(Collectors.toList());
        } catch (InterruptedException e) {
            throw new InterpreterException("Thread execution interrupted: " + e.getMessage());
        }

        // add newly created threads
        prgList.addAll(newPrgList);

        // Print or log after stepping
        for (PrgState prg : prgList) {
            try {
                repo.logPrgStateExec(prg);
            } catch (InterpreterException e) {
                System.out.println("Error logging state: " + e.getMessage());
            }
        }

        if (displayFlag) {
            System.out.println("Current Program States after oneStep:");
            prgList.forEach(System.out::println);
        }

        // update repository
        repo.setPrgList(prgList);
    }

    /**
     * A basic conservative GC that collects addresses from symTables
     * and retains them in the heap.
     */
    private void conservativeGarbageCollector(List<PrgState> prgList) throws InterpreterException {
        if (prgList.isEmpty()) return;

        // gather addresses from symTables
        List<Integer> symAddrs = prgList.stream()
                .flatMap(p -> getAddrFromSymTable(p.getSymTable().values()).stream())
                .collect(Collectors.toList());

        PrgState firstPrg = prgList.get(0); // shared heap
        Map<Integer, Value> heap = firstPrg.getHeap().getContent();

        Map<Integer, Value> newHeap = safeGarbageCollector(symAddrs, heap);
        firstPrg.getHeap().setContent(newHeap);
    }

    private List<Integer> getAddrFromSymTable(Collection<Value> symVals) {
        return symVals.stream()
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
