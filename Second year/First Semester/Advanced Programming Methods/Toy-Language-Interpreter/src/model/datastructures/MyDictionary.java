package model.datastructures;

import exceptions.DictionaryException;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class MyDictionary<K, V> implements MyIDictionary<K, V> {
    private final Map<K, V> dictionary;
    private final MyIHeap heap;

    // Updated constructor to accept a MyIHeap parameter
    public MyDictionary(MyIHeap heap) {
        this.dictionary = new HashMap<>();
        this.heap = heap;
    }

    @Override
    public void add(K key, V value) throws DictionaryException {
        if (dictionary.containsKey(key)) {
            throw new DictionaryException("Key '" + key + "' already exists.");
        }
        dictionary.put(key, value);
    }

    @Override
    public void remove(K key) throws DictionaryException {
        if (!dictionary.containsKey(key)) {
            throw new DictionaryException("Key '" + key + "' does not exist.");
        }
        dictionary.remove(key);
    }

    @Override
    public void update(K key, V value) throws DictionaryException {
        if (!dictionary.containsKey(key)) {
            throw new DictionaryException("Key '" + key + "' does not exist.");
        }
        dictionary.put(key, value);
    }

    @Override
    public boolean isDefined(K key) {
        return dictionary.containsKey(key);
    }

    @Override
    public V lookup(K key) throws DictionaryException {
        if (!dictionary.containsKey(key)) {
            throw new DictionaryException("Variable '" + key + "' is not defined.");
        }
        return dictionary.get(key);
    }

    @Override
    public MyIHeap getHeap() {
        return heap;
    }

    @Override
    public Collection<V> values() {
        return dictionary.values();
    }

    @Override
    public String toString() {
        return dictionary.toString();
    }

    public String toLogString() {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<K, V> entry : dictionary.entrySet()) {
            sb.append(entry.getKey().toString()).append(" --> ").append(entry.getValue().toString()).append("\n");
        }
        return sb.toString();
    }
}
