from colorama import Fore, init
from warehouse import WarehouseSystem
from doubly_linked_list import ConcurrentDoublyLinkedList, run_demo
from scalar_product import run_scalar_product_demo, custom_scalar_product_test

# Initialize colorama for Windows
init()

def print_main_menu():
    print(Fore.GREEN + "=" * 50)
    print(Fore.GREEN + "PARALLEL AND DISTRIBUTED PROGRAMMING LABS")
    print(Fore.GREEN + "=" * 50)
    print(Fore.LIGHTYELLOW_EX + "1.", Fore.BLUE + "Lab 1 - Non-cooperative multithreading")
    print(Fore.LIGHTYELLOW_EX + "2.", Fore.BLUE + "Lab 2 - Producer-Consumer Pattern")
    print(Fore.LIGHTYELLOW_EX + "3.", Fore.RED + "Exit")

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

def main():
    while True:
        print_main_menu()
        choice = input(Fore.CYAN + "Enter your choice (1-3): " + Fore.RESET)
        
        if choice == "1":
            lab1_menu()
        elif choice == "2":
            lab2_menu()
        elif choice == "3":
            print(Fore.RED + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()