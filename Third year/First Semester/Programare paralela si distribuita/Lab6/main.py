from colorama import Fore, init
from warehouse import WarehouseSystem
from doubly_linked_list import ConcurrentDoublyLinkedList, run_demo
from scalar_product import run_scalar_product_demo, custom_scalar_product_test
from matrix_multiplication import run_matrix_multiplication_demo, custom_matrix_test, performance_comparison
from polynomial_multiplication import (
    run_polynomial_demo, custom_polynomial_test, polynomial_performance_comparison,
    run_big_number_demo, custom_big_number_test, big_number_performance_comparison
)
from hamiltonian_cycle import (
    run_hamiltonian_demo, custom_hamiltonian_test, performance_comparison as hamiltonian_performance_comparison
)
import subprocess
import os
import shutil

# Initialize colorama for Windows
init()

def print_main_menu():
    print(Fore.GREEN + "=" * 50)
    print(Fore.GREEN + "PARALLEL AND DISTRIBUTED PROGRAMMING LABS")
    print(Fore.GREEN + "=" * 50)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Lab 1 - Non-cooperative multithreading")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Lab 2 - Producer-Consumer Pattern")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Lab 3 - Matrix Multiplication")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.BLUE + "Lab 5 - Polynomial Multiplication")
    print(Fore.LIGHTYELLOW_EX + "5.", Fore.BLUE + "Lab 6 - Hamiltonian Cycle Finder")
    print(Fore.LIGHTYELLOW_EX + "6.", Fore.RED + "Exit")

def print_lab1_menu():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "Lab 1 - Non-cooperative multithreading")
    print(Fore.CYAN + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Warehouse Problem")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Performance Testing")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.MAGENTA + "Bonus: Doubly-Linked List")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.YELLOW + "Back to Main Menu")

def print_doubly_linked_list_menu():
    print(Fore.MAGENTA + "=" * 40)
    print(Fore.MAGENTA + "BONUS: DOUBLY-LINKED LIST")
    print(Fore.MAGENTA + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Run Concurrent Demo")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Custom Test")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.YELLOW + "Back to Lab 1 Menu")

def doubly_linked_list_menu():
    while True:
        print_doubly_linked_list_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-3): " + Fore.RESET)
        
        if choice == "1":
            print(Fore.GREEN + "Running concurrent doubly-linked list demo...")
            print(Fore.CYAN + "Parameters: 6 threads, 300 operations each")
            run_demo(thread_count=6, ops_per_thread=300)
        elif choice == "2":
            custom_doubly_linked_list_test()
        elif choice == "3":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def custom_doubly_linked_list_test():
    """Custom test with user-defined parameters"""
    try:
        threads = int(input(Fore.CYAN + "Enter number of threads (default 4): " + Fore.RESET) or "4")
        ops = int(input(Fore.CYAN + "Enter operations per thread (default 200): " + Fore.RESET) or "200")
        
        print(Fore.GREEN + f"Running custom test with {threads} threads, {ops} operations each...")
        run_demo(thread_count=threads, ops_per_thread=ops)
        
    except ValueError:
        print(Fore.RED + "Invalid input. Using default values.")
        run_demo(thread_count=4, ops_per_thread=200)

def print_lab2_menu():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "Lab 2 - Producer-Consumer Pattern")
    print(Fore.CYAN + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Scalar Product Demo")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Custom Test")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.YELLOW + "Back to Main Menu")

def print_lab3_menu():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "Lab 3 - Matrix Multiplication")
    print(Fore.CYAN + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Matrix Multiplication Demo")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Custom Test")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Performance Comparison")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.YELLOW + "Back to Main Menu")

def print_lab5_menu():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "Lab 5 - Polynomial Multiplication")
    print(Fore.CYAN + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Polynomial Multiplication Demo")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Custom Polynomial Test")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Polynomial Performance Comparison")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.MAGENTA + "Bonus: Big Number Demo")
    print(Fore.LIGHTYELLOW_EX + "5.", Fore.MAGENTA + "Bonus: Custom Big Number Test")
    print(Fore.LIGHTYELLOW_EX + "6.", Fore.MAGENTA + "Bonus: Big Number Performance Comparison")
    print(Fore.LIGHTYELLOW_EX + "7.", Fore.YELLOW + "Back to Main Menu")

def print_lab6_menu():
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "Lab 6 - Hamiltonian Cycle Finder")
    print(Fore.CYAN + "=" * 40)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Python Implementation - Demo")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Python Implementation - Custom Test")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.BLUE + "Python Implementation - Performance Comparison")
    print(Fore.LIGHTYELLOW_EX + "4.", Fore.MAGENTA + "Java Implementation - Run Demo")
    print(Fore.LIGHTYELLOW_EX + "5.", Fore.YELLOW + "Back to Main Menu")

def lab2_menu():
    while True:
        print_lab2_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-3): " + Fore.RESET)
        
        if choice == "1":
            print(Fore.GREEN + "Running scalar product demo...")
            run_scalar_product_demo()
        elif choice == "2":
            custom_scalar_product_test()
        elif choice == "3":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def lab1_menu():
    while True:
        print_lab1_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-4): " + Fore.RESET)
        
        if choice == "1":
            warehouse_system = WarehouseSystem()
            warehouse_system.run_simulation()
        elif choice == "2":
            warehouse_system = WarehouseSystem()
            warehouse_system.run_performance_tests()
        elif choice == "3":
            doubly_linked_list_menu()
        elif choice == "4":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def lab3_menu():
    while True:
        print_lab3_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-4): " + Fore.RESET)
        
        if choice == "1":
            print(Fore.GREEN + "Running matrix multiplication demo...")
            run_matrix_multiplication_demo()
        elif choice == "2":
            custom_matrix_test()
        elif choice == "3":
            performance_comparison()
        elif choice == "4":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def lab5_menu():
    while True:
        print_lab5_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-7): " + Fore.RESET)
        
        if choice == "1":
            run_polynomial_demo()
        elif choice == "2":
            custom_polynomial_test()
        elif choice == "3":
            polynomial_performance_comparison()
        elif choice == "4":
            run_big_number_demo()
        elif choice == "5":
            custom_big_number_test()
        elif choice == "6":
            big_number_performance_comparison()
        elif choice == "7":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def run_java_hamiltonian():
    """Run the Java implementation of Hamiltonian cycle finder."""
    print(Fore.GREEN + "\nRunning Java implementation...")
    print(Fore.CYAN + "Compiling and running HamiltonianCycle.java...")
    
    java_file = "HamiltonianCycle.java"
    if not os.path.exists(java_file):
        print(Fore.RED + f"Error: {java_file} not found!")
        return
    
    # Find Java installation
    javac_path = None
    java_path = None
    
    # Try to find Java using shutil.which (searches PATH)
    import shutil
    javac_path = shutil.which("javac")
    java_path = shutil.which("java")
    
    # If not found in PATH, search common installation locations
    if not javac_path or not java_path:
        import platform
        if platform.system() == "Windows":
            # Common Java installation paths on Windows
            search_paths = [
                r"C:\Program Files\Microsoft",
                r"C:\Program Files\Java",
                r"C:\Program Files\Eclipse Adoptium",
                r"C:\Program Files (x86)\Java",
            ]
            
            for base_path in search_paths:
                if os.path.exists(base_path):
                    for root, dirs, files in os.walk(base_path):
                        if "javac.exe" in files:
                            javac_path = os.path.join(root, "javac.exe")
                        if "java.exe" in files:
                            java_path = os.path.join(root, "java.exe")
                        if javac_path and java_path:
                            break
                    if javac_path and java_path:
                        break
    
    if not javac_path or not java_path:
        print(Fore.RED + "Error: Java compiler (javac) or Java runtime (java) not found!")
        print(Fore.YELLOW + "Please make sure Java is installed and in your PATH.")
        return
    
    try:
        # Compile Java file
        compile_result = subprocess.run(
            [javac_path, java_file],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if compile_result.returncode != 0:
            print(Fore.RED + "Compilation failed:")
            print(compile_result.stderr)
            return
        
        # Run Java program
        run_result = subprocess.run(
            [java_path, "HamiltonianCycle"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        print(run_result.stdout)
        if run_result.stderr:
            print(Fore.YELLOW + run_result.stderr)
            
    except Exception as e:
        print(Fore.RED + f"Error running Java program: {e}")

def lab6_menu():
    while True:
        print_lab6_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-5): " + Fore.RESET)
        
        if choice == "1":
            run_hamiltonian_demo()
        elif choice == "2":
            custom_hamiltonian_test()
        elif choice == "3":
            hamiltonian_performance_comparison()
        elif choice == "4":
            run_java_hamiltonian()
        elif choice == "5":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def main():
    while True:
        print_main_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-6): " + Fore.RESET)
        
        if choice == "1":
            lab1_menu()
        elif choice == "2":
            lab2_menu()
        elif choice == "3":
            lab3_menu()
        elif choice == "4":
            lab5_menu()
        elif choice == "5":
            lab6_menu()
        elif choice == "6":
            print(Fore.RED + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()