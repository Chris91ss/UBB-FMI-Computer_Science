import threading
import time
import random
from colorama import Fore, init
from collections import deque

init(autoreset=True)


class ThreadSafeQueue:
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.queue = deque()
        self.lock = threading.Lock()
        self.consumer_condition = threading.Condition(self.lock)  # Consumer waits on this
        self.producer_condition = threading.Condition(self.lock)   # Producer waits on this
        self.finished = False  # Signal that producer is done
    
    def put(self, item: float):
        """Put an item in the queue. Blocks if queue is full."""
        with self.producer_condition:
            while len(self.queue) >= self.max_size and not self.finished:
                self.producer_condition.wait()
            
            if not self.finished:
                self.queue.append(item)
                self.consumer_condition.notify()
    
    def get(self) -> float:
        """Get an item from the queue. Blocks if queue is empty."""
        with self.consumer_condition:
            while len(self.queue) == 0 and not self.finished:
                self.consumer_condition.wait()
            
            if len(self.queue) > 0:
                item = self.queue.popleft()
                self.producer_condition.notify()
                return item
            return None  # Producer finished
    
    def mark_finished(self):
        """Mark that the producer is finished adding items."""
        with self.lock:
            self.finished = True
            self.consumer_condition.notify_all()
            self.producer_condition.notify_all()


class ScalarProductComputer:
    """Producer-Consumer pattern for computing scalar product of two vectors."""
    
    def __init__(self, vector1: list, vector2: list, queue_size: int = 10):
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must have the same length")
        
        self.vector1 = vector1
        self.vector2 = vector2
        self.queue = ThreadSafeQueue(queue_size)
        self.result = 0.0
        self.result_lock = threading.Lock()
        self.print_lock = threading.Lock()  
    
    def producer_thread(self):
        """Producer thread: computes element products and feeds the queue."""
        with self.print_lock:
            print(Fore.BLUE + "[Producer] Starting to compute products")
        
        for i, (a, b) in enumerate(zip(self.vector1, self.vector2)):
            product = a * b
            self.queue.put(product)
            with self.print_lock:
                print(Fore.YELLOW + f"[Producer] Computed element {i}: {a} * {b} = {product:.2f}")
        
        self.queue.mark_finished()
        with self.print_lock:
            print(Fore.GREEN + "[Producer] Finished computing all products")
    
    def consumer_thread(self):
        """Consumer thread: sums up products from the queue."""
        with self.print_lock:
            print(Fore.CYAN + "[Consumer] Starting to consume products")
        
        while True:
            product = self.queue.get()
            
            if product is None:  # Producer finished
                break
            
            with self.result_lock:
                self.result += product
            
            with self.print_lock:
                print(Fore.MAGENTA + f"[Consumer] Consumed product: {product:.2f}, running sum: {self.result:.2f}")
        
        with self.print_lock:
            print(Fore.GREEN + "[Consumer] Finished consuming all products")
    
    def compute_scalar_product(self) -> float:
        """Run the producer-consumer computation and return the scalar product."""
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "SCALAR PRODUCT COMPUTATION")
        print(Fore.CYAN + "=" * 50)
        print(Fore.WHITE + f"Vector 1: {self.vector1}")
        print(Fore.WHITE + f"Vector 2: {self.vector2}")
        print(Fore.WHITE + f"Queue size: {self.queue.max_size}")
        print(Fore.CYAN + "=" * 50)
        print()
        
        self.result = 0.0
        
        start_time = time.time()
        
        producer = threading.Thread(target=self.producer_thread)
        consumer = threading.Thread(target=self.consumer_thread)
        
        producer.start()
        consumer.start()
        
        # Wait for both threads to complete
        producer.join()
        consumer.join()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print()
        print(Fore.CYAN + "=" * 50)
        print(Fore.GREEN + "COMPUTATION COMPLETED")
        print(Fore.CYAN + "=" * 50)
        print(Fore.WHITE + f"Scalar product result: {self.result:.6f}")
        print(Fore.WHITE + f"Total time: {elapsed_time:.6f} seconds")
        print(Fore.CYAN + "=" * 50)
        
        return self.result


def generate_random_vectors(size: int) -> tuple:
    """Generate two random vectors of given size."""
    vector1 = [random.uniform(-10.0, 10.0) for _ in range(size)]
    vector2 = [random.uniform(-10.0, 10.0) for _ in range(size)]
    return vector1, vector2


def run_scalar_product_demo():
    """Run a demonstration of the scalar product computation."""
    print(Fore.CYAN + "\n" + "=" * 50)
    print(Fore.CYAN + "SCALAR PRODUCT DEMO")
    print(Fore.CYAN + "=" * 50)
    
    vector1, vector2 = generate_random_vectors(8)
    
    # Test with different queue sizes
    queue_sizes = [1, 3, 5]
    
    for queue_size in queue_sizes:
        print(Fore.YELLOW + f"\n--- Testing with queue size: {queue_size} ---")
        
        computer = ScalarProductComputer(vector1, vector2, queue_size)
        computer.compute_scalar_product()
        print()


def custom_scalar_product_test():
    """Allow user to input custom parameters for testing."""
    try:
        vector_size = int(input(Fore.CYAN + "Enter vector size (default 8): " + Fore.RESET) or "8")
        queue_size = int(input(Fore.CYAN + "Enter queue size (default 5): " + Fore.RESET) or "5")
        
        print(Fore.GREEN + f"Running custom test with vector_size={vector_size}, queue_size={queue_size}")
        
        vector1, vector2 = generate_random_vectors(vector_size)
        
        computer = ScalarProductComputer(vector1, vector2, queue_size)
        computer.compute_scalar_product()
        
    except ValueError:
        print(Fore.RED + "Invalid input. Using default values.")
        run_scalar_product_demo()


if __name__ == "__main__":
    random.seed(42)
    run_scalar_product_demo()
