"""
Threaded implementation of n-body simulation using Barnes-Hut algorithm.
"""
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from .body import Body
from .barnes_hut import BarnesHutTree


class ThreadedSimulator:
    """N-body simulator using multiple threads."""
    
    def __init__(self, bodies, num_threads=4, dt=0.01, G=1.0, theta=0.5):
        """
        Initialize the threaded simulator.
        
        Args:
            bodies: list of Body objects
            num_threads: number of threads to use
            dt: time step
            G: gravitational constant
            theta: Barnes-Hut threshold
        """
        self.bodies = bodies
        self.num_threads = num_threads
        self.dt = dt
        self.G = G
        self.theta = theta
        self.lock = threading.Lock()
        self.tree = None
    
    def step(self):
        """Perform one simulation step."""
        # Build tree (single-threaded, but fast)
        self.tree = BarnesHutTree(self.bodies, self.theta)
        
        # Reset forces
        for body in self.bodies:
            body.reset_force()
        
        # Calculate forces in parallel
        chunk_size = max(1, len(self.bodies) // self.num_threads)
        chunks = [self.bodies[i:i + chunk_size] 
                 for i in range(0, len(self.bodies), chunk_size)]
        
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = []
            for chunk in chunks:
                future = executor.submit(self._calculate_forces_chunk, chunk)
                futures.append(future)
            
            # Wait for all threads to complete
            for future in as_completed(futures):
                future.result()
        
        # Update positions and velocities
        for body in self.bodies:
            body.update_velocity(self.dt)
            body.update_position(self.dt)
    
    def _calculate_forces_chunk(self, chunk):
        """Calculate forces for a chunk of bodies."""
        for body in chunk:
            force = self.tree.calculate_force(body, self.G)
            body.force = force
    
    def run(self, num_steps, display_progress=False):
        """
        Run the simulation for a number of steps.
        
        Args:
            num_steps: number of simulation steps
            display_progress: if True, print progress
        
        Returns:
            list: execution times for each step
        """
        import time
        times = []
        total_elapsed = 0.0
        
        for step in range(num_steps):
            start_time = time.time()
            self.step()
            elapsed = time.time() - start_time
            times.append(elapsed)
            total_elapsed += elapsed
            
            if display_progress:
                from colorama import Fore, Style
                # Show progress every 5 steps or at start/end
                if (step + 1) % 5 == 0 or step == 0 or step == num_steps - 1:
                    print(Fore.GREEN + f"Step {step + 1}/{num_steps} completed (step time: {elapsed:.4f}s, total: {total_elapsed:.2f}s)" + Style.RESET_ALL)
        
        return times

