package controller;

import model.state.PrgState;
import model.stmt.IStmt;
import model.values.Value;
import model.values.RefValue;
import exceptions.ControllerException;
import exceptions.InterpreterException;
import exceptions.StackException;
import exceptions.ADTException;
import repository.IRepository;

import java.util.*;
import java.util.stream.Collectors;

public class Controller {
    private IRepository repo;
    private boolean displayFlag;

    public Controller(IRepository repo) {
        this.repo = repo;
        this.displayFlag = false; // Default is off
    }

    public void setDisplayFlag(boolean flag) {
        this.displayFlag = flag;
    }

    public IRepository getRepo() {
        return this.repo;
    }

    public void oneStep(PrgState state) throws InterpreterException {
        try {
            if (state.getStk().isEmpty()) {
                repo.logPrgStateExec();
                throw new ControllerException("Execution stack is empty");
            }
            IStmt crtStmt = state.getStk().pop();
            crtStmt.execute(state);
            repo.logPrgStateExec(); // Log the program state after each execution step
            if (displayFlag) {
                System.out.println("Current Program State:");
                System.out.println(state.toString());
            }
        } catch (StackException e) {
            throw new ControllerException(e.getMessage());
        } catch (InterpreterException e) {
            throw e;
        }
    }

    public void allStep() throws InterpreterException {
        PrgState state = repo.getCrtPrg();
        while (!state.getStk().isEmpty()) {
            oneStep(state);

            // Perform garbage collection after each execution step
            try {
                conservativeGarbageCollector(state);
            } catch (ADTException e) {
                throw new ControllerException("Garbage Collector error: " + e.getMessage());
            }

            repo.logPrgStateExec(); // Log the program state after garbage collection
            if (displayFlag) {
                System.out.println("Current Program State:");
                System.out.println(state.toString());
            }
        }
    }

    private void conservativeGarbageCollector(PrgState state) throws ADTException {
        Collection<Value> symTableValues = state.getSymTable().values(); // Use the values() method
        Map<Integer, Value> heapContent = state.getHeap().getContent();

        // Get addresses from the symbol table
        Set<Integer> symTableAddresses = getAddressesFromValues(symTableValues);

        // Compute the set of all reachable addresses
        Set<Integer> reachableAddresses = getReachableAddresses(symTableAddresses, heapContent);

        // Perform garbage collection
        Map<Integer, Value> newHeapContent = heapContent.entrySet().stream()
                .filter(entry -> reachableAddresses.contains(entry.getKey()))
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

        state.getHeap().setContent(newHeapContent);
    }

    private Set<Integer> getAddressesFromValues(Collection<Value> values) {
        Set<Integer> addresses = new HashSet<>();
        for (Value value : values) {
            if (value instanceof RefValue) {
                addresses.add(((RefValue) value).getAddr());
            }
        }
        return addresses;
    }

    private Set<Integer> getReachableAddresses(Set<Integer> addresses, Map<Integer, Value> heap) {
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> toVisit = new Stack<>();
        toVisit.addAll(addresses);

        while (!toVisit.isEmpty()) {
            int address = toVisit.pop();
            if (!visited.contains(address)) {
                visited.add(address);
                Value value = heap.get(address);
                if (value instanceof RefValue) {
                    int newAddr = ((RefValue) value).getAddr();
                    if (!visited.contains(newAddr)) {
                        toVisit.push(newAddr);
                    }
                }
            }
        }
        return visited;
    }
}
