"""
MPI distributed implementation of n-body simulation using Barnes-Hut algorithm.
"""
import numpy as np
from mpi4py import MPI
from .body import Body
from .barnes_hut import BarnesHutTree


class MPISimulator:
    """N-body simulator using MPI for distributed computing."""
    
    def __init__(self, bodies, dt=0.01, G=1.0, theta=0.5):
        """
        Initialize the MPI simulator.
        
        Args:
            bodies: list of Body objects (all ranks should have same initial bodies)
            dt: time step
            G: gravitational constant
            theta: Barnes-Hut threshold
        """
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        
        self.bodies = bodies
        self.dt = dt
        self.G = G
        self.theta = theta
        
        # Distribute bodies across ranks
        self._distribute_bodies()
    
    def _distribute_bodies(self):
        """Distribute bodies across MPI ranks."""
        total_bodies = len(self.bodies)
        bodies_per_rank = total_bodies // self.size
        remainder = total_bodies % self.size
        
        # Calculate local range
        start_idx = self.rank * bodies_per_rank + min(self.rank, remainder)
        end_idx = start_idx + bodies_per_rank + (1 if self.rank < remainder else 0)
        
        self.local_bodies = self.bodies[start_idx:end_idx]
        self.local_indices = list(range(start_idx, end_idx))
    
    def _gather_all_bodies(self):
        """Gather all body positions from all ranks."""
        # Collect positions and velocities from all ranks (flatten for MPI)
        local_positions = np.array([body.position for body in self.local_bodies]).flatten()
        local_velocities = np.array([body.velocity for body in self.local_bodies]).flatten()
        local_masses = np.array([body.mass for body in self.local_bodies])
        
        # Calculate counts for each rank (in elements, not bodies)
        total_bodies = len(self.bodies)
        bodies_per_rank = total_bodies // self.size
        remainder = total_bodies % self.size
        
        # Build counts and displacements arrays
        counts_pos = []
        counts_vel = []
        counts_mass = []
        displs = []
        offset = 0
        
        for r in range(self.size):
            num_bodies_r = bodies_per_rank + (1 if r < remainder else 0)
            counts_pos.append(num_bodies_r * 3)  # 3 doubles per body
            counts_vel.append(num_bodies_r * 3)  # 3 doubles per body
            counts_mass.append(num_bodies_r)     # 1 double per body
            displs.append(offset * 3)
            offset += num_bodies_r
        
        # Gather data from all ranks
        all_positions = None
        all_velocities = None
        all_masses = None
        
        if self.rank == 0:
            all_positions = np.zeros(len(self.bodies) * 3, dtype=np.float64)
            all_velocities = np.zeros(len(self.bodies) * 3, dtype=np.float64)
            all_masses = np.zeros(len(self.bodies), dtype=np.float64)
        
        # Gather positions (flattened)
        self.comm.Gatherv(local_positions, 
                         [all_positions, tuple(counts_pos), tuple(displs), MPI.DOUBLE] if self.rank == 0 else None,
                         root=0)
        
        # Gather velocities (flattened)
        self.comm.Gatherv(local_velocities,
                         [all_velocities, tuple(counts_vel), tuple(displs), MPI.DOUBLE] if self.rank == 0 else None,
                         root=0)
        
        # Gather masses
        displs_mass = [d // 3 for d in displs]  # Convert position displacement to body count
        self.comm.Gatherv(local_masses,
                         [all_masses, tuple(counts_mass), tuple(displs_mass), MPI.DOUBLE] if self.rank == 0 else None,
                         root=0)
        
        # Broadcast to all ranks
        if self.rank != 0:
            all_positions = np.zeros(len(self.bodies) * 3, dtype=np.float64)
            all_velocities = np.zeros(len(self.bodies) * 3, dtype=np.float64)
            all_masses = np.zeros(len(self.bodies), dtype=np.float64)
        
        self.comm.Bcast(all_positions, root=0)
        self.comm.Bcast(all_velocities, root=0)
        self.comm.Bcast(all_masses, root=0)
        
        # Reshape and update all bodies with gathered data
        all_positions = all_positions.reshape(len(self.bodies), 3)
        all_velocities = all_velocities.reshape(len(self.bodies), 3)
        
        for i, body in enumerate(self.bodies):
            body.position = all_positions[i]
            body.velocity = all_velocities[i]
            body.mass = all_masses[i]
    
    def step(self):
        """Perform one simulation step."""
        # Synchronize all bodies across ranks
        self._gather_all_bodies()
        
        # Build tree from all bodies (each rank builds its own)
        tree = BarnesHutTree(self.bodies, self.theta)
        
        # Reset forces for local bodies
        for body in self.local_bodies:
            body.reset_force()
        
        # Calculate forces for local bodies
        for body in self.local_bodies:
            force = tree.calculate_force(body, self.G)
            body.force = force
        
        # Update velocities and positions for local bodies
        for body in self.local_bodies:
            body.update_velocity(self.dt)
            body.update_position(self.dt)
        
        # Synchronize again to share updated positions
        self._gather_all_bodies()
    
    def run(self, num_steps, display_progress=False):
        """
        Run the simulation for a number of steps.
        
        Args:
            num_steps: number of simulation steps
            display_progress: if True, print progress (only rank 0)
        
        Returns:
            list: execution times for each step (only rank 0)
        """
        import time
        times = []
        total_elapsed = 0.0
        
        for step in range(num_steps):
            start_time = time.time()
            self.step()
            elapsed = time.time() - start_time
            
            # Synchronize timing
            elapsed = self.comm.allreduce(elapsed, op=MPI.MAX)
            times.append(elapsed)
            total_elapsed += elapsed
            
            if display_progress and self.rank == 0:
                from colorama import Fore, Style
                # Show progress every 5 steps or at start/end
                if (step + 1) % 5 == 0 or step == 0 or step == num_steps - 1:
                    print(Fore.GREEN + f"Step {step + 1}/{num_steps} completed (step time: {elapsed:.4f}s, total: {total_elapsed:.2f}s)" + Style.RESET_ALL)
        
        return times if self.rank == 0 else []

