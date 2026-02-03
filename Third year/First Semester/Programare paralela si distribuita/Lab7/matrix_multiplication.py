import threading
import time
import random
from colorama import Fore, init
from typing import List, Tuple

init(autoreset=True)


def compute_matrix_element(A: List[List[float]], B: List[List[float]], 
                          row: int, col: int) -> float:
    n = len(A[0])
    result = 0.0
    
    for k in range(n):
        result += A[row][k] * B[k][col]
    
    return result


def row_wise_thread_worker(A: List[List[float]], B: List[List[float]], 
                           result: List[List[float]], thread_id: int, 
                           num_threads: int, print_lock: threading.Lock):
    rows = len(result)
    cols = len(result[0])
    total_elements = rows * cols
    elements_per_thread = total_elements // num_threads
    start_index = thread_id * elements_per_thread
    end_index = start_index + elements_per_thread if thread_id < num_threads - 1 else total_elements
    
    computed = 0
    for index in range(start_index, end_index):
        row = index // cols
        col = index % cols
        
        # Compute element outside the lock (parallel work)
        value = compute_matrix_element(A, B, row, col)
        
        # Only lock for printing and storing result
        with print_lock:
            result[row][col] = value
            print(Fore.CYAN + f"Thread {thread_id}: Computing element ({row}, {col}) = {value:.2f}", flush=True)
        computed += 1
    
    with print_lock:
        print(Fore.GREEN + f"Thread {thread_id} completed: {computed} elements (row-wise distribution)", flush=True)


def column_wise_thread_worker(A: List[List[float]], B: List[List[float]], 
                              result: List[List[float]], thread_id: int, 
                              num_threads: int, print_lock: threading.Lock):
    rows = len(result)
    cols = len(result[0])
    total_elements = rows * cols
    elements_per_thread = total_elements // num_threads
    start_index = thread_id * elements_per_thread
    end_index = start_index + elements_per_thread if thread_id < num_threads - 1 else total_elements
    
    computed = 0
    for index in range(start_index, end_index):
        # Column-wise: row = index % rows, col = index // rows
        row = index % rows
        col = index // rows
        
        # Compute element outside the lock (parallel work)
        value = compute_matrix_element(A, B, row, col)
        
        # Only lock for printing and storing result
        with print_lock:
            result[row][col] = value
            print(Fore.CYAN + f"Thread {thread_id}: Computing element ({row}, {col}) = {value:.2f}", flush=True)
        computed += 1
    
    with print_lock:
        print(Fore.GREEN + f"Thread {thread_id} completed: {computed} elements (column-wise distribution)", flush=True)


def kth_element_thread_worker(A: List[List[float]], B: List[List[float]], 
                              result: List[List[float]], thread_id: int, 
                              num_threads: int, print_lock: threading.Lock):
    rows = len(result)
    cols = len(result[0])
    total_elements = rows * cols
    computed = 0
    
    # k-th element: thread_id, thread_id + num_threads, thread_id + 2*num_threads, ...
    for index in range(thread_id, total_elements, num_threads):
        row = index // cols
        col = index % cols
        
        # Compute element outside the lock (parallel work)
        value = compute_matrix_element(A, B, row, col)
        
        # Only lock for printing and storing result
        with print_lock:
            result[row][col] = value
            print(Fore.CYAN + f"Thread {thread_id}: Computing element ({row}, {col}) = {value:.2f}", flush=True)
        computed += 1
    
    with print_lock:
        print(Fore.GREEN + f"Thread {thread_id} completed: {computed} elements (k-th element distribution)", flush=True)


def generate_random_matrix(rows: int, cols: int, min_val: float = 1.0, max_val: float = 10.0) -> List[List[float]]:
    return [[random.uniform(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


def matrix_multiply_parallel(A: List[List[float]], B: List[List[float]], 
                            num_threads: int, distribution: str = "row_wise") -> Tuple[List[List[float]], float]:
    rows = len(A)
    cols = len(B[0])
    
    # Initialize result matrix
    result = [[0.0 for _ in range(cols)] for _ in range(rows)]
    
    # Lock for synchronized printing
    print_lock = threading.Lock()
    
    # Select the appropriate worker function
    if distribution == "row_wise":
        worker_func = row_wise_thread_worker
    elif distribution == "column_wise":
        worker_func = column_wise_thread_worker
    elif distribution == "kth_element":
        worker_func = kth_element_thread_worker
    else:
        raise ValueError(f"Unknown distribution: {distribution}")
    
    # Create and start threads
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_func,
            args=(A, B, result, i, num_threads, print_lock)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time


    


def run_matrix_multiplication_demo():
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "MATRIX MULTIPLICATION DEMO")
    print(Fore.GREEN + "=" * 60)
    
    # Demo parameters
    matrix_size = 9
    num_threads = 4
    
    print(Fore.CYAN + f"\nMatrix size: {matrix_size}x{matrix_size}")
    print(Fore.CYAN + f"Number of threads: {num_threads}\n")
    
    # Generate random matrices
    print(Fore.YELLOW + "Generating random matrices...")
    A = generate_random_matrix(matrix_size, matrix_size)
    B = generate_random_matrix(matrix_size, matrix_size)
    
    distributions = ["row_wise", "column_wise", "kth_element"]
    
    for dist in distributions:
        print(Fore.MAGENTA + "\n" + "=" * 60)
        print(Fore.MAGENTA + f"Distribution Strategy: {dist.upper().replace('_', '-')}")
        print(Fore.MAGENTA + "=" * 60)
        
        result, exec_time = matrix_multiply_parallel(A, B, num_threads, dist)
        print(Fore.YELLOW + f"\nExecution time: {exec_time:.4f} seconds")


def custom_matrix_test():
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "CUSTOM MATRIX MULTIPLICATION TEST")
    print(Fore.GREEN + "=" * 60)
    
    try:
        rows_A = int(input(Fore.CYAN + "Enter number of rows for matrix A (default 6): " + Fore.RESET) or "6")
        cols_A = int(input(Fore.CYAN + "Enter number of columns for matrix A (default 6): " + Fore.RESET) or "6")
        rows_B = int(input(Fore.CYAN + "Enter number of rows for matrix B (default 6): " + Fore.RESET) or "6")
        cols_B = int(input(Fore.CYAN + "Enter number of columns for matrix B (default 6): " + Fore.RESET) or "6")
        num_threads = int(input(Fore.CYAN + "Enter number of threads (default 4): " + Fore.RESET) or "4")
        
        if cols_A != rows_B:
            print(Fore.RED + "Error: Number of columns in A must equal number of rows in B!")
            return
        
        print(Fore.CYAN + "\nSelect distribution strategy:")
        print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Row-wise consecutive")
        print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Column-wise consecutive")
        print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "k-th element")
        
        choice = input(Fore.CYAN + "Enter choice (1-3, default 1): " + Fore.RESET) or "1"
        
        distribution_map = {"1": "row_wise", "2": "column_wise", "3": "kth_element"}
        distribution = distribution_map.get(choice, "row_wise")
        
        print(Fore.YELLOW + f"\nMatrix A: {rows_A}x{cols_A}, Matrix B: {rows_B}x{cols_B}")
        print(Fore.YELLOW + f"Result matrix: {rows_A}x{cols_B}")
        print(Fore.YELLOW + f"Threads: {num_threads}, Strategy: {distribution.replace('_', '-')}")
        print(Fore.YELLOW + "Generating random matrices...\n")
        
        A = generate_random_matrix(rows_A, cols_A)
        B = generate_random_matrix(rows_B, cols_B)
        
        result, exec_time = matrix_multiply_parallel(A, B, num_threads, distribution)
        print(Fore.YELLOW + f"\nExecution time: {exec_time:.4f} seconds")
            
    except ValueError as e:
        print(Fore.RED + f"Invalid input: {e}")


def performance_comparison():
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + "PERFORMANCE COMPARISON")
    print(Fore.GREEN + "=" * 60)
    
    # Test configurations: (matrix_size, num_threads)
    # Increased sizes for more reliable performance signals
    test_configs = [
        (100, 2),
        (100, 100),
        (200, 4),
        (200, 100),
        (300, 4),
        (300, 100),
        (400, 4),
        (400, 100),
    ]
    
    distributions = ["row_wise", "column_wise", "kth_element"]
    
    print(Fore.CYAN + "\nRunning performance tests (without debug printing)...\n")
    
    results = []
    
    for size, threads in test_configs:
        print(Fore.YELLOW + f"Testing: {size}x{size} matrix with {threads} threads")
        
        # Generate matrices once per configuration
        A = generate_random_matrix(size, size)
        B = generate_random_matrix(size, size)
        
        config_results = {"size": size, "threads": threads}
        
        for dist in distributions:
            # Temporarily disable debug printing for performance tests
            # We'll create a modified version without printing
            result, exec_time = matrix_multiply_parallel_no_print(A, B, threads, dist)
            config_results[dist] = exec_time
        
        results.append(config_results)
    
    # Print summary table
    print(Fore.GREEN + "\n" + "=" * 80)
    print(Fore.GREEN + "PERFORMANCE SUMMARY")
    print(Fore.GREEN + "=" * 80)
    print(Fore.CYAN + f"{'Size':<10} {'Threads':<10} {'Row-wise':<15} {'Column-wise':<15} {'k-th element':<15}")
    print(Fore.CYAN + "-" * 80)
    
    for res in results:
        print(Fore.YELLOW + f"{res['size']:<10} {res['threads']:<10} "
              f"{res['row_wise']:<15.4f} {res['column_wise']:<15.4f} {res['kth_element']:<15.4f}")
    
    print()


def matrix_multiply_parallel_no_print(A: List[List[float]], B: List[List[float]], 
                                     num_threads: int, distribution: str = "row_wise") -> Tuple[List[List[float]], float]:
    rows = len(A)
    cols = len(B[0])
    result = [[0.0 for _ in range(cols)] for _ in range(rows)]
    print_lock = threading.Lock()
    
    def compute_element_no_print(A, B, row, col):
        n = len(A[0])
        result = 0.0
        for k in range(n):
            result += A[row][k] * B[k][col]
        return result
    
    def row_wise_no_print(A, B, result, thread_id, num_threads, print_lock):
        rows = len(result)
        cols = len(result[0])
        total_elements = rows * cols
        elements_per_thread = total_elements // num_threads
        start_index = thread_id * elements_per_thread
        end_index = start_index + elements_per_thread if thread_id < num_threads - 1 else total_elements
        
        for index in range(start_index, end_index):
            row = index // cols
            col = index % cols
            result[row][col] = compute_element_no_print(A, B, row, col)
    
    def column_wise_no_print(A, B, result, thread_id, num_threads, print_lock):
        rows = len(result)
        cols = len(result[0])
        total_elements = rows * cols
        elements_per_thread = total_elements // num_threads
        start_index = thread_id * elements_per_thread
        end_index = start_index + elements_per_thread if thread_id < num_threads - 1 else total_elements
        
        for index in range(start_index, end_index):
            row = index % rows
            col = index // rows
            result[row][col] = compute_element_no_print(A, B, row, col)
    
    def kth_element_no_print(A, B, result, thread_id, num_threads, print_lock):
        rows = len(result)
        cols = len(result[0])
        total_elements = rows * cols
        
        for index in range(thread_id, total_elements, num_threads):
            row = index // cols
            col = index % cols
            result[row][col] = compute_element_no_print(A, B, row, col)
    
    worker_map = {
        "row_wise": row_wise_no_print,
        "column_wise": column_wise_no_print,
        "kth_element": kth_element_no_print
    }
    
    worker_func = worker_map[distribution]
    
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(target=worker_func, args=(A, B, result, i, num_threads, print_lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time

