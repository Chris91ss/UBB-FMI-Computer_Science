package model.datastructures;

import exceptions.DictionaryException;

import java.util.Collection;

public interface MyIDictionary<K, V> {
    void add(K key, V value) throws DictionaryException;
    void remove(K key) throws DictionaryException;
    void update(K key, V value) throws DictionaryException;
    boolean isDefined(K key);
    V lookup(K key) throws DictionaryException;
    MyIHeap getHeap();
    Collection<V> values();
    String toString();
    String toLogString();
}