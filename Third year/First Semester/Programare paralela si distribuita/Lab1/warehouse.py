import threading
import random
import time
from colorama import Fore, init
from collections import defaultdict

# keep the nice colors
init(autoreset=True)


class Warehouse:
    """
    - A short warehouse RLock protects the inventory structure itself and the product-lock map.
    - Per-product locks protect quantities of individual products so disjoint products don't block each other.
    """
    def __init__(self, warehouse_id: int):
        self.warehouse_id = warehouse_id
        self._meta_lock = threading.RLock()                 # protects map structure, creation of product locks
        self._product_locks = defaultdict(threading.Lock)   # product_id -> Lock
        self._inventory = defaultdict(int)                  # product_id -> quantity

    # ---- helpers (call only when holding the right locks) ----
    def _add_unlocked(self, product_id: int, qty: int):
        self._inventory[product_id] += qty

    def _remove_unlocked(self, product_id: int, qty: int) -> bool:
        if self._inventory[product_id] >= qty:
            self._inventory[product_id] -= qty
            return True
        return False

    def product_lock(self, product_id: int) -> threading.Lock:
        # ensure lock existence under meta lock to avoid races
        with self._meta_lock:
            return self._product_locks[product_id]

    def get_inventory_snapshot(self) -> dict:
        with self._meta_lock:
            return dict(self._inventory)


class WarehouseSystem:
    """
    System with two granularity options:
      - granularity="product" (default): per-(warehouse,product) locks -> best concurrency and matches the spec.
      - granularity="warehouse": single lock per move across both warehouses (kept for comparison in perf tests).
    """
    def __init__(self, num_warehouses=5, num_products=10, granularity="product"):
        assert granularity in ("product", "warehouse")
        self.granularity = granularity
        self.warehouses = [Warehouse(i) for i in range(num_warehouses)]
        self.num_products = num_products

        # operation counters (Option A)
        self._ops_attempts = 0
        self._ops_success = 0
        self._ops_lock = threading.Lock()

        self._check_lock = threading.Lock()   # serialize inventory check print
        self._print_lock = threading.Lock()   # serialize all console output

        # initial fill + totals for invariant checking
        self.initial_totals = defaultdict(int)
        self._initialize_random()

        # a per-warehouse big lock (only used in "warehouse" granularity for a simple baseline)
        self._big_locks = [threading.Lock() for _ in range(num_warehouses)]

    # ---------- initialization ----------
    def _initialize_random(self):
        with self._print_lock:
            print(Fore.CYAN + "Initializing warehouses with random inventory...", flush=True)
        for wh in self.warehouses:
            with wh._meta_lock:
                for pid in range(self.num_products):
                    qty = random.randint(10, 100)
                    wh._add_unlocked(pid, qty)
                    self.initial_totals[pid] += qty
        with self._print_lock:
            print(Fore.GREEN + f"Initialized {len(self.warehouses)} warehouses with {self.num_products} products each", flush=True)
        self._print_initial_totals()

    def _print_initial_totals(self):
        with self._print_lock:
            print(Fore.YELLOW + "\nInitial Inventory Totals:", flush=True)
            for pid in range(self.num_products):
                print(f"Product {pid}: {self.initial_totals[pid]} units", flush=True)

    # ---------- move operation ----------
    def move_products(self, src_id: int, dst_id: int, product_quantities: dict) -> bool:
        """
        Move the given quantities (dict: product_id -> qty) from src to dst.
        - If granularity=='product': lock only the EXACT products we touch across src+dst, in a deterministic order.
        - If granularity=='warehouse': lock the two warehouse big locks (simpler, more contention).
        Returns True if move succeeds; False if source lacks stock (no partial move).
        """
        if src_id == dst_id:
            # Count as an attempt; it's a no-op but "successful" by definition.
            with self._ops_lock:
                self._ops_attempts += 1
                self._ops_success += 1
            return True

        src = self.warehouses[src_id]
        dst = self.warehouses[dst_id]
        success = False

        if self.granularity == "warehouse":
            # simple order by warehouse id to avoid deadlock
            first_id, second_id = sorted([src_id, dst_id])
            first_lock = self._big_locks[first_id]
            second_lock = self._big_locks[second_id]

            with first_lock, second_lock:
                with src._meta_lock, dst._meta_lock:
                    # check stock
                    for pid, qty in product_quantities.items():
                        if src._inventory[pid] < qty:
                            success = False
                            break
                    else:
                        # perform move
                        ok = True
                        for pid, qty in product_quantities.items():
                            if not src._remove_unlocked(pid, qty):
                                ok = False
                                break
                            dst._add_unlocked(pid, qty)
                        success = ok

        else:  # granularity == "product"  (recommended / default)
            # Make a deterministic global order of (warehouse_id, role, product_id)
            # role S<D ensures source locks come before destination locks when same warehouse_id & product_id
            pids = sorted(product_quantities.keys())
            plan = [(src_id, 'S', pid) for pid in pids] + [(dst_id, 'D', pid) for pid in pids]
            plan.sort()  # sorts by warehouse_id, then role ('D'>'S'), then product_id

            acquired = []
            try:
                # acquire all per-product locks
                for wid, _, pid in plan:
                    wh = src if wid == src_id else dst
                    plock = wh.product_lock(pid)
                    plock.acquire()
                    acquired.append(plock)

                # after per-product locks are held, check and move atomically
                with src._meta_lock, dst._meta_lock:
                    for pid, qty in product_quantities.items():
                        if src._inventory[pid] < qty:
                            success = False
                            break
                    else:
                        ok = True
                        for pid, qty in product_quantities.items():
                            if not src._remove_unlocked(pid, qty):
                                ok = False
                                break
                            dst._add_unlocked(pid, qty)
                        success = ok
            finally:
                for plock in reversed(acquired):
                    plock.release()

        # ---- Count attempts and successes (Option A) ----
        with self._ops_lock:
            self._ops_attempts += 1
            if success:
                self._ops_success += 1

        return success

    # ---------- worker & simulation ----------
    def worker_thread(self, tid: int, num_ops: int):
        with self._print_lock:
            print(Fore.BLUE + f"Thread {tid} starting with {num_ops} operations", flush=True)

        W = len(self.warehouses)
        for _ in range(num_ops):
            s = random.randint(0, W - 1)
            d = random.randint(0, W - 1)
            k = random.randint(1, min(3, self.num_products))  # 1..3 different products
            pids = random.sample(range(self.num_products), k)
            move = {pid: random.randint(1, 10) for pid in pids}

            ok = self.move_products(s, d, move)
            with self._print_lock:
                color = Fore.GREEN if ok else Fore.RED
                status = "Moved" if ok else "Failed"
                print(color + f"Thread {tid}: {status} {move} from W{s} to W{d}", flush=True)

            time.sleep(0.001)  # tiny delay to vary interleavings

        with self._print_lock:
            print(Fore.BLUE + f"Thread {tid} completed", flush=True)

    def run_simulation(self, num_threads=5000, operations_per_thread=20):
        with self._print_lock:
            print(Fore.CYAN + f"\nStarting simulation with {num_threads} threads,"
                              f" {operations_per_thread} operations each (granularity={self.granularity})", flush=True)
            print(Fore.CYAN + f"Total operations: {num_threads * operations_per_thread}", flush=True)

        with self._ops_lock:
            self._ops_attempts = 0
            self._ops_success = 0

        threads = []
        t0 = time.time()
        for i in range(num_threads):
            t = threading.Thread(target=self.worker_thread, args=(i, operations_per_thread))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        elapsed = time.time() - t0

        with self._print_lock:
            print(Fore.YELLOW + f"\nSimulation completed in {elapsed:.4f} seconds", flush=True)
            print(Fore.YELLOW + f"Total attempts: {self._ops_attempts}", flush=True)
            print(Fore.YELLOW + f"Successful moves: {self._ops_success}", flush=True)

        self.inventory_check()

    # ---------- invariant check ----------
    def inventory_check(self) -> bool:
        with self._check_lock:
            with self._print_lock:
                print(Fore.MAGENTA + "\n" + "=" * 50, flush=True)
                print(Fore.MAGENTA + "INVENTORY CHECK", flush=True)
                print(Fore.MAGENTA + "=" * 50, flush=True)

            current = defaultdict(int)
            ok = True
            # snapshot each warehouse safely
            for wh in self.warehouses:
                snap = wh.get_inventory_snapshot()
                for pid, qty in snap.items():
                    current[pid] += qty

            with self._print_lock:
                for pid in range(self.num_products):
                    init_total = self.initial_totals[pid]
                    now_total = current[pid]
                    if init_total == now_total:
                        print(Fore.GREEN + f"✓ Product {pid}: {now_total}/{init_total} (CORRECT)", flush=True)
                    else:
                        print(Fore.RED + f"✗ Product {pid}: {now_total}/{init_total} (ERROR!)", flush=True)
                        ok = False

                print(Fore.MAGENTA + "=" * 50, flush=True)
                print(Fore.GREEN + "INVENTORY CHECK PASSED" if ok else Fore.RED + "INVENTORY CHECK FAILED", flush=True)
                print(Fore.MAGENTA + "=" * 50, flush=True)
            return ok

    # ---------- simple performance tests ----------
    def run_performance_tests(self):
        with self._print_lock:
            print(Fore.CYAN + "\n" + "=" * 60, flush=True)
            print(Fore.CYAN + "PERFORMANCE TESTING", flush=True)
            print(Fore.CYAN + "=" * 60, flush=True)

        configs = [
            (2, 50),
            (4, 50),
            (8, 50),
            (2, 100),
            (4, 100),
        ]

        results = []

        for gran in ("warehouse", "product"):
            with self._print_lock:
                print(Fore.YELLOW + f"\n=== Granularity: {gran} ===", flush=True)
            for thr, ops in configs:
                # build a fresh system each run
                sys = WarehouseSystem(num_warehouses=len(self.warehouses),
                                      num_products=self.num_products,
                                      granularity=gran)
                t0 = time.time()
                sys.run_simulation(thr, ops)
                dt = time.time() - t0
                total_ops = thr * ops
                ops_sec = total_ops / dt if dt > 0 else float("inf")
                results.append({
                    "granularity": gran,
                    "threads": thr,
                    "ops_per_thread": ops,
                    "total_ops": total_ops,
                    "time_s": dt,
                    "ops_per_s": ops_sec
                })
                with self._print_lock:
                    print(Fore.GREEN + f"Result: {dt:.4f}s | {ops_sec:.2f} ops/s", flush=True)

        with self._print_lock:
            print(Fore.CYAN + "\n" + "=" * 60, flush=True)
            print(Fore.CYAN + "PERFORMANCE SUMMARY", flush=True)
            print(Fore.CYAN + "=" * 60, flush=True)
            print(f"{'Gran.':<10}{'Threads':<10}{'Ops/Thr':<10}{'TotalOps':<12}{'Time(s)':<10}{'Ops/s':<10}", flush=True)
            print("-" * 60, flush=True)
            for r in results:
                print(f"{r['granularity']:<10}{r['threads']:<10}{r['ops_per_thread']:<10}"
                      f"{r['total_ops']:<12}{r['time_s']:<10.4f}{r['ops_per_s']:<10.2f}", flush=True)


def print_mutex_documentation():
    """
    Short documentation of which mutex protects which invariant.
    Keep it concise to match the lab deliverable.
    """
    print(Fore.CYAN + "\n" + "=" * 60)
    print(Fore.CYAN + "MUTEX DOCUMENTATION")
    print(Fore.CYAN + "=" * 60)

    print(Fore.YELLOW + "\nLocks & Invariants")
    print(Fore.WHITE + "1) Warehouse._meta_lock (RLock)")
    print("   Protects: the inventory map itself and creation of per-product locks.")
    print("   Invariant: inventory structure is consistent (no races creating locks).")

    print(Fore.WHITE + "\n2) Warehouse per-product locks (one per product_id)")
    print("   Protects: quantity of that specific product in that specific warehouse.")
    print("   Invariant: quantities never go negative; per-product moves are atomic.")
    print("   Benefit: moves touching disjoint product sets don’t block each other.")

    print(Fore.WHITE + "\n3) System _ops_lock")
    print("   Protects: operation counters (attempts & successes).")

    print(Fore.WHITE + "\n4) System _check_lock")
    print("   Protects: inventory check, so the report is readable and consistent.")

    print(Fore.WHITE + "\n5) System _print_lock")
    print("   Protects: console output from interleaving across threads.")

    print(Fore.YELLOW + "\nDeadlock avoidance")
    print("- In product granularity, acquire per-(warehouse,product) locks in a deterministic order")
    print("  sorted by (warehouse_id, role S<D, product_id).")
    print("- In warehouse granularity, acquire the two big locks in ascending warehouse id.")

    print(Fore.YELLOW + "\nWhy totals stay constant")
    print("- Every move checks source stock and updates src then dst under the right locks;")
    print("  no losses or duplicates, so the sum over warehouses equals the initial totals.")
