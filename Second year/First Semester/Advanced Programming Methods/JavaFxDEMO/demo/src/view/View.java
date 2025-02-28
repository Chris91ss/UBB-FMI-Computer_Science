package view;

import controller.Controller;
import exceptions.InterpreterException;
import model.datastructures.*;
import model.state.PrgState;
import model.stmt.IStmt;
import model.values.StringValue;
import model.values.Value;
import repository.IRepository;
import repository.Repository;

import java.io.BufferedReader;
import java.util.List;
import java.util.Scanner;

public class View {
    private List<IStmt> programs;

    public View(List<IStmt> programs) {
        this.programs = programs;
    }

    public void menu() {
        System.out.println("Toy Language Interpreter Menu:");
        for (int i = 0; i < programs.size(); i++) {
            System.out.println((i + 1) + ". Run example program " + (i + 1));
        }
        System.out.println("0. Exit");
        System.out.println();
    }

    public void run() {
        Scanner scanner = new Scanner(System.in);
        int option;

        while (true) {
            menu();
            System.out.print("Enter your option: ");
            option = scanner.nextInt();

            if (option == 0) {
                System.out.println("Exiting interpreter. Goodbye!");
                break;
            }

            if (option < 1 || option > programs.size()) {
                System.out.println("Invalid option. Please choose between 0 and " + programs.size() + ".");
            } else {
                // Ask the user if they want to display the program state after each step
                System.out.print("Display program state after each execution step? (yes/no): ");
                String displayOption = scanner.next();
                boolean displayFlag = displayOption.equalsIgnoreCase("yes") || displayOption.equalsIgnoreCase("y");

                IStmt selectedProgram = programs.get(option - 1);
                executeProgram(selectedProgram, displayFlag);
            }
            System.out.println();
        }

        scanner.close();
    }

    private void executeProgram(IStmt program, boolean displayFlag) {
        try {
            // Initialize data structures for the program state
            MyIStack<IStmt> exeStack = new MyStack<>();
            // Initialize the heap
            MyIHeap heap = new MyHeap();
            // Pass the heap to the symbol table and file table
            MyIDictionary<String, Value> symTable = new MyDictionary<>(heap);
            MyIDictionary<StringValue, BufferedReader> fileTable = new MyDictionary<>(heap);
            MyIList<Value> out = new MyList<>();

            // Create the initial program state with the selected program
            PrgState prgState = new PrgState(exeStack, symTable, heap, out, fileTable, program);

            // Create the repository and controller for this execution
            String logFilePath = "log.txt"; // You can customize the log file path
            IRepository repo = new Repository(prgState, logFilePath);
            Controller controller = new Controller(repo);

            // Set the display flag
            controller.setDisplayFlag(displayFlag);

            // Execute the program
            controller.allStep();

            // Display the final program state and output
            System.out.println("Final Program State:");
            System.out.println(prgState.toString());
            System.out.println("Output:");
            System.out.println(out.toString());
        } catch (InterpreterException e) {
            System.out.println("Execution failed: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("An unexpected error occurred: " + e.getMessage());
        }
    }
}
