"""
Main entry point for n-body simulation with interactive menu.
"""
import numpy as np
import sys
import os
from colorama import Fore, Style, init
from src.body import Body
from src.threaded_sim import ThreadedSimulator
from src.mpi_sim import MPISimulator

# Initialize colorama
init(autoreset=True)


def generate_random_bodies(num_bodies, seed=42):
    """Generate random initial conditions for bodies."""
    np.random.seed(seed)
    bodies = []
    
    for _ in range(num_bodies):
        # Random position in cube [-10, 10]^3
        position = np.random.uniform(-10, 10, 3)
        # Random velocity
        velocity = np.random.uniform(-0.1, 0.1, 3)
        # Random mass
        mass = np.random.uniform(0.1, 1.0)
        bodies.append(Body(position, velocity, mass))
    
    return bodies


def display_bodies(bodies, max_display=10):
    """Display body information in a formatted table."""
    print("\n" + Fore.CYAN + "="*80)
    print(Fore.YELLOW + "BODY INFORMATION")
    print(Fore.CYAN + "="*80 + Style.RESET_ALL)
    print(f"{'Index':<8} {'X':<12} {'Y':<12} {'Z':<12} {'VX':<12} {'VY':<12} {'VZ':<12} {'Mass':<10}")
    print(Fore.CYAN + "-"*80 + Style.RESET_ALL)
    
    display_count = min(len(bodies), max_display)
    for i in range(display_count):
        body = bodies[i]
        print(f"{i:<8} {body.position[0]:<12.4f} {body.position[1]:<12.4f} "
              f"{body.position[2]:<12.4f} {body.velocity[0]:<12.4f} "
              f"{body.velocity[1]:<12.4f} {body.velocity[2]:<12.4f} {body.mass:<10.4f}")
    
    if len(bodies) > max_display:
        print(Fore.YELLOW + f"... ({len(bodies) - max_display} more bodies)" + Style.RESET_ALL)
    
    print(Fore.CYAN + "="*80 + Style.RESET_ALL + "\n")


def display_performance(times, num_bodies, num_steps):
    """Display performance metrics."""
    import sys
    total_time = sum(times)
    avg_time = total_time / len(times) if times else 0
    min_time = min(times) if times else 0
    max_time = max(times) if times else 0
    
    print("\n" + Fore.CYAN + "="*80)
    print(Fore.YELLOW + "PERFORMANCE METRICS")
    print(Fore.CYAN + "="*80 + Style.RESET_ALL)
    print(f"Number of bodies: {Fore.GREEN}{num_bodies}{Style.RESET_ALL}")
    print(f"Number of steps: {Fore.GREEN}{num_steps}{Style.RESET_ALL}")
    print(f"Total execution time: {Fore.GREEN}{total_time:.4f} seconds{Style.RESET_ALL}")
    print(f"Average time per step: {Fore.GREEN}{avg_time:.4f} seconds{Style.RESET_ALL}")
    print(f"Min time per step: {Fore.GREEN}{min_time:.4f} seconds{Style.RESET_ALL}")
    print(f"Max time per step: {Fore.GREEN}{max_time:.4f} seconds{Style.RESET_ALL}")
    print(f"Throughput: {Fore.GREEN}{num_bodies * num_steps / total_time:.2f} body-steps/second{Style.RESET_ALL}")
    print(Fore.CYAN + "="*80 + Style.RESET_ALL + "\n")
    sys.stdout.flush()  # Ensure output is displayed immediately
    
    return {
        'num_bodies': num_bodies,
        'num_steps': num_steps,
        'total_time': total_time,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'throughput': num_bodies * num_steps / total_time if total_time > 0 else 0
    }


def save_results_to_file(bodies, performance, sim_type, filename=None):
    """Save simulation results to a text file."""
    from datetime import datetime
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{sim_type}_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("N-BODY SIMULATION RESULTS\n")
            f.write(f"Simulation Type: {sim_type}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # Performance metrics
            f.write("PERFORMANCE METRICS\n")
            f.write("-"*80 + "\n")
            f.write(f"Number of bodies: {performance['num_bodies']}\n")
            f.write(f"Number of steps: {performance['num_steps']}\n")
            f.write(f"Total execution time: {performance['total_time']:.4f} seconds\n")
            f.write(f"Average time per step: {performance['avg_time']:.4f} seconds\n")
            f.write(f"Min time per step: {performance['min_time']:.4f} seconds\n")
            f.write(f"Max time per step: {performance['max_time']:.4f} seconds\n")
            f.write(f"Throughput: {performance['throughput']:.2f} body-steps/second\n")
            f.write("\n" + "="*80 + "\n\n")
            
            # Body information
            f.write("BODY INFORMATION\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Index':<8} {'X':<12} {'Y':<12} {'Z':<12} {'VX':<12} {'VY':<12} {'VZ':<12} {'Mass':<10}\n")
            f.write("-"*80 + "\n")
            
            for i, body in enumerate(bodies):
                f.write(f"{i:<8} {body.position[0]:<12.4f} {body.position[1]:<12.4f} "
                       f"{body.position[2]:<12.4f} {body.velocity[0]:<12.4f} "
                       f"{body.velocity[1]:<12.4f} {body.velocity[2]:<12.4f} {body.mass:<10.4f}\n")
            
            f.write("="*80 + "\n")
        
        print(Fore.GREEN + f"\nResults saved to: {filename}" + Style.RESET_ALL)
        return filename
    except Exception as e:
        print(Fore.RED + f"\nError saving results: {e}" + Style.RESET_ALL)
        return None


def run_threaded_simulation():
    """Run threaded simulation."""
    print("\n" + Fore.CYAN + "="*60)
    print(Fore.YELLOW + "  THREADED SIMULATION")
    print(Fore.CYAN + "="*60 + Style.RESET_ALL)
    print()
    
    # Configuration
    try:
        num_bodies = int(input("Enter number of bodies (default 1000): ") or "1000")
        num_threads = int(input("Enter number of threads (default 4): ") or "4")
        num_steps = int(input("Enter number of steps (default 100): ") or "100")
    except ValueError:
        print("Invalid input. Using default values.")
        num_bodies = 1000
        num_threads = 4
        num_steps = 100
    
    # Generate bodies
    print(f"\nGenerating {num_bodies} bodies...")
    bodies = generate_random_bodies(num_bodies)
    
    # Create simulator
    simulator = ThreadedSimulator(bodies, num_threads=num_threads)
    
    # Run simulation
    print(Fore.GREEN + f"\nRunning simulation with {num_threads} threads for {num_steps} steps..." + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 60 + Style.RESET_ALL)
    times = simulator.run(num_steps, display_progress=True)
    
    # Display results
    display_bodies(bodies)
    performance = display_performance(times, num_bodies, num_steps)
    
    # Save to file
    save_results_to_file(bodies, performance, "Threaded")
    
    input("\nPress Enter to return to menu...")


def run_mpi_simulation():
    """Run MPI simulation."""
    from mpi4py import MPI
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if rank == 0:
        print("\n" + Fore.CYAN + "="*60)
        print(Fore.YELLOW + "  MPI SIMULATION")
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        print(Fore.GREEN + f"\nRunning with {size} MPI process(es)" + Style.RESET_ALL)
        print()
        
        # Configuration (only rank 0 reads input)
        try:
            num_bodies = int(input("Enter number of bodies (default 1000): ") or "1000")
            num_steps = int(input("Enter number of steps (default 100): ") or "100")
        except ValueError:
            print("Invalid input. Using default values.")
            num_bodies = 1000
            num_steps = 100
    else:
        num_bodies = None
        num_steps = None
    
    # Broadcast configuration
    num_bodies = comm.bcast(num_bodies, root=0)
    num_steps = comm.bcast(num_steps, root=0)
    
    if rank == 0:
        print(f"\nGenerating {num_bodies} bodies...")
        bodies = generate_random_bodies(num_bodies)
    else:
        bodies = None
    
    # Broadcast bodies to all ranks
    if rank == 0:
        # Pack body data
        positions = np.array([b.position for b in bodies])
        velocities = np.array([b.velocity for b in bodies])
        masses = np.array([b.mass for b in bodies])
    else:
        positions = np.zeros((num_bodies, 3))
        velocities = np.zeros((num_bodies, 3))
        masses = np.zeros(num_bodies)
    
    comm.Bcast(positions, root=0)
    comm.Bcast(velocities, root=0)
    comm.Bcast(masses, root=0)
    
    # Reconstruct bodies on all ranks
    if rank != 0:
        bodies = [Body(positions[i], velocities[i], masses[i]) for i in range(num_bodies)]
    
    # Create simulator
    simulator = MPISimulator(bodies)
    
    if rank == 0:
        print(Fore.GREEN + f"\nRunning simulation with {size} MPI processes for {num_steps} steps..." + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 60 + Style.RESET_ALL)
    
    # Run simulation
    times = simulator.run(num_steps, display_progress=(rank == 0))
    
    # Display results (only rank 0)
    if rank == 0:
        display_bodies(bodies)
        performance = display_performance(times, num_bodies, num_steps)
        
        # Save to file
        save_results_to_file(bodies, performance, f"MPI_{size}processes")
        
        input("\nPress Enter to return to menu...")


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main menu loop."""
    while True:
        clear_screen()
        print("\n" + Fore.CYAN + "="*60)
        print(Fore.YELLOW + "  N-BODY SIMULATION - BARNES-HUT ALGORITHM")
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        print()
        print(Fore.GREEN + "  1. Run Threaded Simulation")
        print(Fore.GREEN + "  2. Run MPI Simulation")
        print(Fore.RED + "  3. Exit")
        print()
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            try:
                run_threaded_simulation()
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\nSimulation interrupted by user." + Style.RESET_ALL)
                input("Press Enter to continue...")
            except Exception as e:
                print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == "2":
            try:
                run_mpi_simulation()
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\nSimulation interrupted by user." + Style.RESET_ALL)
                input("Press Enter to continue...")
            except Exception as e:
                print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
                print(Fore.YELLOW + "\nNote: Run with: mpirun -n <num_processes> python main.py" + Style.RESET_ALL)
                input("\nPress Enter to continue...")
        elif choice == "3":
            print(Fore.GREEN + "\nExiting... Goodbye!" + Style.RESET_ALL)
            sys.exit(0)
        else:
            print(Fore.RED + "\nInvalid choice. Please enter 1, 2, or 3." + Style.RESET_ALL)
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

