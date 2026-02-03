import threading
import random
import time
from colorama import Fore, init
from typing import Optional, Any, List, Tuple

init(autoreset=True)


class _Node:
    """Internal node for a doubly-linked list with its own lock."""
    __slots__ = ("value", "prev", "next", "lock", "is_sentinel")

    def __init__(self, value: Any = None, is_sentinel: bool = False):
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None
        self.lock = threading.RLock()
        self.is_sentinel = is_sentinel

    def __repr__(self):
        if self.is_sentinel:
            return f"<Sentinel>"
        return f"<Node {self.value}>"


class ConcurrentDoublyLinkedList:
    """
    Concurrent doubly-linked list with per-node locking (no central mutex).
    Inserts use lock-coupling + validate-and-retry to avoid splicing with stale neighbors.
    """

    def __init__(self, iterable: Optional[List[Any]] = None):
        self.head = _Node(is_sentinel=True)
        self.tail = _Node(is_sentinel=True)
        self.head.next = self.tail
        self.tail.prev = self.head

        if iterable:
            last = self.head
            for v in iterable:
                n = _Node(v)
                n.prev = last
                n.next = self.tail
                last.next = n
                self.tail.prev = n
                last = n

    # -------------------- Core operations --------------------

    def move_next(self, node: _Node) -> Optional[_Node]:
        """Move to the next node (returns None if at the end)."""
        with node.lock:
            nxt = node.next
            if nxt and not nxt.is_sentinel:
                print(Fore.CYAN + f"[{threading.get_ident()}] move_next: {node} → {nxt}")
                return nxt
            return None

    def move_prev(self, node: _Node) -> Optional[_Node]:
        """Move to the previous node (returns None if at the head)."""
        with node.lock:
            prev = node.prev
            if prev and not prev.is_sentinel:
                print(Fore.CYAN + f"[{threading.get_ident()}] move_prev: {node} → {prev}")
                return prev
            return None

    def insert_after(self, node: _Node, value: Any) -> _Node:
        """Insert a new node immediately after the given one with validation/retry."""
        if node is self.tail:
            raise ValueError("Cannot insert after tail sentinel.")

        new_node = _Node(value)

        backoff = 0.0001
        while True:
            # Step 1: read neighbor (optimistically)
            nxt = node.next

            # Step 2: lock in deterministic order: node -> nxt
            with node.lock:
                # neighbor might have changed while we were waiting; refresh
                nxt = node.next
                if nxt is None:
                    # Shouldn't happen with sentinels, but handle gracefully
                    nxt = self.tail

                # Lock nxt second
                with nxt.lock:
                    # Step 3: validate the adjacency we plan to splice into
                    if node.next is not nxt or nxt.prev is not node:
                        # Adjacency changed under our feet; retry
                        print(Fore.LIGHTBLACK_EX + f"[{threading.get_ident()}] insert_after retry: adjacency changed")
                    else:
                        # Step 4: splice
                        print(Fore.YELLOW + f"[{threading.get_ident()}] insert_after: inserting {new_node} after {node}")
                        new_node.prev = node
                        new_node.next = nxt
                        node.next = new_node
                        nxt.prev = new_node
                        print(Fore.GREEN + f"[{threading.get_ident()}] insert_after COMPLETE: {new_node} linked.")
                        return new_node

            # Small backoff to avoid live-lock under extreme contention
            time.sleep(backoff)
            backoff = min(backoff * 2, 0.005)

    def insert_before(self, node: _Node, value: Any) -> _Node:
        """Insert a new node immediately before the given one with validation/retry."""
        if node is self.head:
            raise ValueError("Cannot insert before head sentinel.")

        new_node = _Node(value)

        backoff = 0.0001
        while True:
            # Step 1: read neighbor (optimistically)
            prev = node.prev
            if prev is None:
                # Corruption/edge case; retry after small wait
                time.sleep(backoff)
                backoff = min(backoff * 2, 0.005)
                continue

            # Step 2: lock in deterministic order: prev -> node
            with prev.lock:
                with node.lock:
                    # Step 3: validate the adjacency we plan to splice into
                    if prev.next is not node or node.prev is not prev:
                        print(Fore.LIGHTBLACK_EX + f"[{threading.get_ident()}] insert_before retry: adjacency changed")
                    else:
                        # Step 4: splice
                        print(Fore.YELLOW + f"[{threading.get_ident()}] insert_before: inserting {new_node} before {node}")
                        new_node.prev = prev
                        new_node.next = node
                        prev.next = new_node
                        node.prev = new_node
                        print(Fore.GREEN + f"[{threading.get_ident()}] insert_before COMPLETE: {new_node} linked.")
                        return new_node

            time.sleep(backoff)
            backoff = min(backoff * 2, 0.005)

    # -------------------- Helpers --------------------

    def to_list(self) -> List[Any]:
        out = []
        cur = self.head.next
        while cur and not cur.is_sentinel:
            out.append(cur.value)
            cur = cur.next
        return out

    def find_kth(self, k: int) -> Optional[_Node]:
        cur = self.head.next
        i = 0
        while cur and not cur.is_sentinel:
            if i == k:
                return cur
            i += 1
            cur = cur.next
        return None

    # -------------------- Invariant check --------------------

    def check_structure(self) -> Tuple[bool, str]:
        """
        Verify internal consistency:
          - forward links match backward links
          - no cycles (simple seen-set)
        Call after all worker threads have joined.
        """
        # Forward traversal
        seen = set()
        cur = self.head
        last = None
        while cur:
            if cur in seen:
                return (False, "Cycle detected (forward)")
            seen.add(cur)
            nxt = cur.next
            if nxt:
                if nxt.prev is not cur:
                    return (False, f"Broken prev pointer between {cur} and {nxt}")
            last = cur
            cur = nxt
            if last is self.tail:
                break

        # Backward traversal
        seen = set()
        cur = self.tail
        last = None
        while cur:
            if cur in seen:
                return (False, "Cycle detected (backward)")
            seen.add(cur)
            prv = cur.prev
            if prv:
                if prv.next is not cur:
                    return (False, f"Broken next pointer between {prv} and {cur}")
            last = cur
            cur = prv
            if last is self.head:
                break

        return (True, "OK")


# -------------------- Concurrent demo --------------------

def _worker_demo(dll: ConcurrentDoublyLinkedList, tid: int, ops: int):
    # Random starting point
    base_list = dll.to_list()
    start_idx = random.randint(0, max(0, len(base_list) - 1)) if base_list else 0
    cur = dll.find_kth(start_idx) or dll.head

    for _ in range(ops):
        action = random.choice(["next", "prev", "after", "before"])
        try:
            if action == "next":
                n = dll.move_next(cur)
                if n:
                    cur = n
            elif action == "prev":
                p = dll.move_prev(cur)
                if p:
                    cur = p
            elif action == "after":
                if cur is dll.tail:
                    continue
                cur = dll.insert_after(cur, f"T{tid}-A-{random.randint(0,999)}")
            else:  # before
                if cur is dll.head:
                    continue
                cur = dll.insert_before(cur, f"T{tid}-B-{random.randint(0,999)}")
        except Exception as e:
            print(Fore.RED + f"[{threading.get_ident()}] Exception: {e}")
        time.sleep(0.0005)  # tiny delay to mix interleavings


def run_demo(thread_count: int = 6, ops_per_thread: int = 300):
    print(Fore.MAGENTA + "=" * 40)
    print(Fore.MAGENTA + "Concurrent Doubly-Linked List Demo")
    print(Fore.MAGENTA + "=" * 40)
    print(Fore.CYAN + f"Starting {thread_count} threads, {ops_per_thread} operations each...\n")

    dll = ConcurrentDoublyLinkedList([f"seed-{i}" for i in range(8)])

    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=_worker_demo, args=(dll, i, ops_per_thread))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(Fore.MAGENTA + "\n" + "=" * 40)
    print(Fore.MAGENTA + "STRUCTURE CHECK")
    print(Fore.MAGENTA + "=" * 40)
    ok, msg = dll.check_structure()
    if ok:
        print(Fore.GREEN + f"Structure consistent ✅ ({msg})")
    else:
        print(Fore.RED + f"Structure check failed ❌ ({msg})")

    snapshot = dll.to_list()[:20]
    print(Fore.YELLOW + f"List snapshot (first 20): {snapshot}")
    print(Fore.MAGENTA + "=" * 40)


if __name__ == "__main__":
    random.seed(42)
    run_demo(thread_count=6, ops_per_thread=300)
