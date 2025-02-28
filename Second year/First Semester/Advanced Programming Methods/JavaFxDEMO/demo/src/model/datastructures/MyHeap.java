package model.datastructures;

import model.values.Value;
import exceptions.ADTException;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;
import java.util.concurrent.atomic.AtomicInteger;

public class MyHeap implements MyIHeap {
    private Map<Integer, Value> heap;
    private final AtomicInteger nextFreeAddress;
    private final Stack<Integer> freeAddresses;

    public MyHeap() {
        this.heap = new HashMap<>();
        this.nextFreeAddress = new AtomicInteger(1); // Addresses start from 1
        this.freeAddresses = new Stack<>(); // Stack to store free addresses
    }

    @Override
    public int allocate(Value value) {
        int address;

        if (!freeAddresses.isEmpty()) {
            // Reuse an address from the pool of free addresses
            address = freeAddresses.pop();
        } else {
            // Allocate a new address
            address = nextFreeAddress.getAndIncrement();
        }

        heap.put(address, value);
        return address;
    }

    @Override
    public Value deallocate(int address) throws ADTException {
        if (!heap.containsKey(address)) {
            throw new ADTException("Heap deallocation error: Address " + address + " not found.");
        }
        Value value = heap.remove(address);
        freeAddresses.push(address); // Add the deallocated address to the pool
        return value;
    }

    @Override
    public Value get(int address) throws ADTException {
        if (!heap.containsKey(address)) {
            throw new ADTException("Heap retrieval error: Address " + address + " not found.");
        }
        return heap.get(address);
    }

    @Override
    public boolean containsKey(int address) {
        return heap.containsKey(address);
    }

    @Override
    public void update(int address, Value value) throws ADTException {
        if (!heap.containsKey(address)) {
            throw new ADTException("Heap update error: Address " + address + " not found.");
        }
        heap.put(address, value);
    }

    @Override
    public Map<Integer, Value> getContent() {
        return heap;
    }

    @Override
    public void setContent(Map<Integer, Value> newContent) {
        heap = newContent;
        // Recompute free addresses based on the new content
        recomputeFreeAddresses();
    }

    private void recomputeFreeAddresses() {
        freeAddresses.clear();
        int maxAddress = nextFreeAddress.get();

        // Collect all used addresses
        boolean[] usedAddresses = new boolean[maxAddress];
        for (Integer address : heap.keySet()) {
            if (address < maxAddress) {
                usedAddresses[address] = true;
            }
        }

        // Add unused addresses to the freeAddresses stack
        for (int i = 1; i < maxAddress; i++) {
            if (!usedAddresses[i]) {
                freeAddresses.push(i);
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<Integer, Value> entry : heap.entrySet()) {
            sb.append(entry.getKey()).append("->").append(entry.getValue().toString()).append("\n");
        }
        return sb.toString();
    }

    @Override
    public String toLogString() {
        return this.toString();
    }
}
