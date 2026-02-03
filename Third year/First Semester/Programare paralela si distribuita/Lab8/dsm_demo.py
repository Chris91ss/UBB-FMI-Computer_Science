"""
DSM Demo Script

This script demonstrates the Distributed Shared Memory (DSM) mechanism.
It should be run with MPI, e.g.: mpiexec -n 3 python dsm_demo.py
"""

import time
import threading
from mpi4py import MPI
from dsm import DSM, Subscriber


def sleep_for_milliseconds(milliseconds: int):
    """Sleep for the specified number of milliseconds"""
    time.sleep(milliseconds / 1000.0)


def variable_change_callback(variable: int, old_value: int, new_value: int):
    """
    Callback function that is called when a variable changes.
    All processes receive callbacks in the same order.
    """
    rank = MPI.COMM_WORLD.Get_rank()
    print(f"[Rank {rank}] CALLBACK: Variable {variable} changed from {old_value} to {new_value}")


def main():
    """Main function that runs the DSM demo"""
    # Check if MPI is already initialized (e.g., by mpiexec)
    if not MPI.Is_initialized():
        MPI.Init()
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Get DSM singleton instance
    dsm = DSM.getInstance()
    
    # Register callback for variable changes
    dsm.register_callback(1, variable_change_callback)
    dsm.register_callback(2, variable_change_callback)
    dsm.register_callback(3, variable_change_callback)
    
    # Create subscriber and run it in a separate thread
    subscriber = Subscriber(dsm)
    subscriber_thread = threading.Thread(target=subscriber.run, daemon=False)
    subscriber_thread.start()
    
    print(f"[Rank {rank}] Started process {rank} of {size}")
    
    # Synchronize all processes
    comm.Barrier()
    
    if rank == 0:
        # Process 0: Master process
        print(f"\n[Rank {rank}] Master process starting operations...")
        
        # Subscribe to variables 1, 2, 3
        dsm.subscribeTo(1)
        dsm.subscribeTo(2)
        dsm.subscribeTo(3)
        
        sleep_for_milliseconds(4000)
        
        # Check and replace: if variable 1 == 0, set it to 10
        dsm.checkAndReplace(1, 0, 10)
        
        sleep_for_milliseconds(3000)
        
        # Check and replace: if variable 3 == 2, set it to 30
        dsm.checkAndReplace(3, 2, 30)
        
        sleep_for_milliseconds(3000)
        
        # Check and replace: if variable 2 == 100, set it to 20 (should not execute)
        dsm.checkAndReplace(2, 100, 20)
        
        sleep_for_milliseconds(3000)
        
        # Close all processes
        dsm.close()
        
        sleep_for_milliseconds(1000)
        
        # Wait for subscriber thread to finish
        subscriber_thread.join()
        
        print(f"\n[Rank {rank}] Master process finished")
    
    elif rank == 1:
        # Process 1: Subscribe to variables 1 and 3
        print(f"\n[Rank {rank}] Process 1 starting operations...")
        
        dsm.subscribeTo(1)
        dsm.subscribeTo(3)
        
        sleep_for_milliseconds(8000)
        
        subscriber_thread.join()
        
        print(f"\n[Rank {rank}] Process 1 finished")
    
    elif rank == 2:
        # Process 2: Subscribe to variable 2
        print(f"\n[Rank {rank}] Process 2 starting operations...")
        
        dsm.subscribeTo(2)
        
        sleep_for_milliseconds(9000)
        
        # Check and replace: if variable 2 == 1, set it to 50
        dsm.checkAndReplace(2, 1, 50)
        
        sleep_for_milliseconds(1000)
        
        subscriber_thread.join()
        
        print(f"\n[Rank {rank}] Process 2 finished")
    
    else:
        # Additional processes (if any) just wait
        print(f"\n[Rank {rank}] Additional process waiting...")
        subscriber_thread.join()
        print(f"\n[Rank {rank}] Process {rank} finished")
    
    # Only finalize if we initialized it (not if mpiexec did)
    if MPI.Is_initialized() and not MPI.Is_finalized():
        MPI.Finalize()


if __name__ == "__main__":
    main()

