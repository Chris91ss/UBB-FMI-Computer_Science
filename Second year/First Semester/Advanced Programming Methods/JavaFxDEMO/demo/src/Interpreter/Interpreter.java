package Interpreter;

import controller.Controller;
import model.datastructures.*;
import model.exp.*;
import model.state.PrgState;
import model.stmt.*;
import model.types.*;
import model.values.*;
import repository.IRepository;
import repository.Repository;
import view.*;

import java.io.BufferedReader;
import exceptions.StatementException;
import exceptions.ExpressionException;
import exceptions.DictionaryException;
import view.gui.ProgramSelectionApp;

public class Interpreter {
    public static void main(String[] args) {
        ProgramSelectionApp.main(args);
    }
}

    /*
    public static void main(String[] args) {
        // Initialize examples
        IStmt ex1 = initializeExample1();
        IStmt ex2 = initializeExample2();
        IStmt ex3 = initializeExample3();
        IStmt ex4 = initializeExample4();
        IStmt ex5 = initializeExample5();
        IStmt ex6 = initializeExample6();
        IStmt ex7 = initializeExample7();
        IStmt ex8 = initializeExample8();
        IStmt ex9 = initializeExample9();
        IStmt ex10 = initializeExample10();

        // Create the Text Menu
        TextMenu menu = new TextMenu();
        menu.addCommand(new ExitCommand("0", "exit"));

        // Initialize and add examples to the menu
        initializeAndAddToMenu("1", ex1, "int v; v=2; Print(v)", menu);
        initializeAndAddToMenu("2", ex2, "int a; int b; a=2+3*5; b=a+1; Print(b)", menu);
        initializeAndAddToMenu("3", ex3, "bool a; a=false; int v; If a Then v=2 Else v=3; Print(v)", menu);
        initializeAndAddToMenu("4", ex4, "File operations test: " + ex4.toString(), menu);
        initializeAndAddToMenu("5", ex5, "Using relational expressions: " + ex5.toString(), menu);
        initializeAndAddToMenu("6", ex6, "int v; v=4; while (v>0) { print(v); v=v-1; } print(v);", menu);
        initializeAndAddToMenu("7", ex7, "Testing the Heap: " + ex7.toString(), menu);
        initializeAndAddToMenu("8", ex8, "Testing the Garbage Collector: " + ex8.toString(), menu);
        initializeAndAddToMenu("9", ex9, "Concurrency and Heap Operations: " + ex9.toString(), menu);
        initializeAndAddToMenu("10", ex10, "Type Error Example: " + ex10.toString(), menu);

        // Display the menu and wait for user input
        menu.show();
    }

    private static void initializeAndAddToMenu(String key, IStmt stmt, String description, TextMenu menu) {
        // Create a fresh heap for the type environment
        MyIHeap typeHeap = new MyHeap();
        // Create the type environment dictionary with the heap
        MyIDictionary<String, Type> typeEnv = new MyDictionary<>(typeHeap);

        try {
            // Perform type checking
            stmt.typecheck(typeEnv);
        } catch (StatementException | ExpressionException | DictionaryException e) {
            System.out.println("Type Checking Failed for Example " + key + ": " + e.getMessage());
            return; // Skip adding this example to the menu
        }

        // Initialize the actual heap for the program
        MyIHeap programHeap = new MyHeap();

        // Initialize Program State
        PrgState prg = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(programHeap),
                programHeap,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(programHeap), // FileTable
                stmt
        );

        // Initialize Repository and Controller
        IRepository repo = new Repository(prg, "log" + key + ".txt");
        Controller ctr = new Controller(repo);

        // Add the example to the menu
        menu.addCommand(new RunExample(key, description, ctr));
    }

    // Helper methods to initialize each example statement
    private static IStmt initializeExample1() {
        // Example 1: int v; v=2; Print(v)
        return new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new AssignStmt("v", new ValueExp(new IntValue(2))),
                        new PrintStmt(new VarExp("v"))
                )
        );
    }

    private static IStmt initializeExample2() {
        // Example 2: int a; int b; a=2+3*5; b=a+1; Print(b)
        return new CompStmt(
                new VarDeclStmt("a", new IntType()),
                new CompStmt(
                        new VarDeclStmt("b", new IntType()),
                        new CompStmt(
                                new AssignStmt("a", new ArithExp(
                                        1, // '+'
                                        new ValueExp(new IntValue(2)),
                                        new ArithExp(
                                                3, // '*'
                                                new ValueExp(new IntValue(3)),
                                                new ValueExp(new IntValue(5))
                                        )
                                )),
                                new CompStmt(
                                        new AssignStmt("b", new ArithExp(
                                                1, // '+'
                                                new VarExp("a"),
                                                new ValueExp(new IntValue(1))
                                        )),
                                        new PrintStmt(new VarExp("b"))
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample3() {
        // Example 3: bool a; a=false; int v; If a Then v=2 Else v=3; Print(v)
        return new CompStmt(
                new VarDeclStmt("a", new BoolType()),
                new CompStmt(
                        new AssignStmt("a", new ValueExp(new BoolValue(false))),
                        new CompStmt(
                                new VarDeclStmt("v", new IntType()),
                                new CompStmt(
                                        new IfStmt(
                                                new VarExp("a"),
                                                new AssignStmt("v", new ValueExp(new IntValue(2))),
                                                new AssignStmt("v", new ValueExp(new IntValue(3)))
                                        ),
                                        new PrintStmt(new VarExp("v"))
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample4() {
        // Example 4: File operations test
        return new CompStmt(
                new VarDeclStmt("varf", new StringType()),
                new CompStmt(
                        new AssignStmt("varf", new ValueExp(new StringValue("test.in"))),
                        new CompStmt(
                                new OpenRFile(new VarExp("varf")),
                                new CompStmt(
                                        new VarDeclStmt("varc", new IntType()),
                                        new CompStmt(
                                                new ReadFile(new VarExp("varf"), "varc"),
                                                new CompStmt(
                                                        new PrintStmt(new VarExp("varc")),
                                                        new CompStmt(
                                                                new ReadFile(new VarExp("varf"), "varc"),
                                                                new CompStmt(
                                                                        new PrintStmt(new VarExp("varc")),
                                                                        new CloseRFile(new VarExp("varf"))
                                                                )
                                                        )
                                                )
                                        )
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample5() {
        // Example 5: Using relational expressions
        return new CompStmt(
                new VarDeclStmt("a", new IntType()),
                new CompStmt(
                        new VarDeclStmt("b", new IntType()),
                        new CompStmt(
                                new AssignStmt("a", new ValueExp(new IntValue(10))),
                                new CompStmt(
                                        new AssignStmt("b", new ValueExp(new IntValue(20))),
                                        new CompStmt(
                                                new IfStmt(
                                                        new RelationalExp("<", new VarExp("a"), new VarExp("b")),
                                                        new PrintStmt(new ValueExp(new StringValue("a < b"))),
                                                        new PrintStmt(new ValueExp(new StringValue("a >= b")))
                                                ),
                                                new CompStmt(
                                                        new IfStmt(
                                                                new RelationalExp(">", new ArithExp(2, new VarExp("a"), new ValueExp(new IntValue(5))), new VarExp("b")),
                                                                new PrintStmt(new ValueExp(new StringValue("a - 5 > b"))),
                                                                new PrintStmt(new ValueExp(new StringValue("a - 5 <= b")))
                                                        ),
                                                        new CompStmt(
                                                                new IfStmt(
                                                                        new RelationalExp("==", new VarExp("a"), new VarExp("b")),
                                                                        new PrintStmt(new ValueExp(new StringValue("a == b"))),
                                                                        new PrintStmt(new ValueExp(new StringValue("a != b")))
                                                                ),
                                                                new PrintStmt(new ValueExp(new StringValue("End of relational expression tests")))
                                                        )
                                                )
                                        )
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample6() {
        // Example 6: int v; v=4; while (v>0) { print(v); v=v-1; } print(v);
        return new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new AssignStmt("v", new ValueExp(new IntValue(4))),
                        new CompStmt(
                                new WhileStmt(
                                        new RelationalExp(">", new VarExp("v"), new ValueExp(new IntValue(0))),
                                        new CompStmt(
                                                new PrintStmt(new VarExp("v")),
                                                new AssignStmt("v", new ArithExp(2, new VarExp("v"), new ValueExp(new IntValue(1))))
                                        )
                                ),
                                new PrintStmt(new VarExp("v"))
                        )
                )
        );
    }

    private static IStmt initializeExample7() {
        // Example 7: Testing the Heap
        return new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new VarDeclStmt("a", new RefType(new IntType())),
                        new CompStmt(
                                new AssignStmt("v", new ValueExp(new IntValue(10))),
                                new CompStmt(
                                        new NewStmt("a", new VarExp("v")),
                                        new CompStmt(
                                                new PrintStmt(new ReadHeapExp(new VarExp("a"))),
                                                new CompStmt(
                                                        new WriteHeapStmt("a", new ValueExp(new IntValue(20))),
                                                        new PrintStmt(new ReadHeapExp(new VarExp("a")))
                                                )
                                        )
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample8() {
        // Example 8: Testing the Garbage Collector
        return new CompStmt(
                new VarDeclStmt("a", new RefType(new IntType())),
                new CompStmt(
                        new VarDeclStmt("b", new RefType(new IntType())),
                        new CompStmt(
                                new NewStmt("a", new ValueExp(new IntValue(10))),
                                new CompStmt(
                                        new NewStmt("b", new ValueExp(new IntValue(20))),
                                        new CompStmt(
                                                new PrintStmt(new ReadHeapExp(new VarExp("a"))),
                                                new CompStmt(
                                                        new PrintStmt(new ReadHeapExp(new VarExp("b"))),
                                                        new CompStmt(
                                                                new AssignStmt("a", new VarExp("b")), // a = b
                                                                new CompStmt(
                                                                        new PrintStmt(new ReadHeapExp(new VarExp("a"))),
                                                                        new PrintStmt(new ReadHeapExp(new VarExp("b")))
                                                                )
                                                        )
                                                )
                                        )
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample9() {
        // Example 9:
        // int v; Ref int a; v=10; new(a,22);
        // fork(wH(a,30); v=32; Print(v); Print(rH(a)));
        // Print(v); Print(rH(a))
        return new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new VarDeclStmt("a", new RefType(new IntType())),
                        new CompStmt(
                                new AssignStmt("v", new ValueExp(new IntValue(10))),
                                new CompStmt(
                                        new NewStmt("a", new ValueExp(new IntValue(22))),
                                        new CompStmt(
                                                new forkStmt(
                                                        new CompStmt(
                                                                new WriteHeapStmt("a", new ValueExp(new IntValue(30))),
                                                                new CompStmt(
                                                                        new AssignStmt("v", new ValueExp(new IntValue(32))),
                                                                        new CompStmt(
                                                                                new PrintStmt(new VarExp("v")),
                                                                                new PrintStmt(new ReadHeapExp(new VarExp("a")))
                                                                        )
                                                                )
                                                        )
                                                ),
                                                new CompStmt(
                                                        new PrintStmt(new VarExp("v")),
                                                        new PrintStmt(new ReadHeapExp(new VarExp("a")))
                                                )
                                        )
                                )
                        )
                )
        );
    }

    private static IStmt initializeExample10() {
        // Example 10: Type Error - Assigning a boolean to an integer variable
        return new CompStmt(
                new VarDeclStmt("x", new IntType()),                      // Declare x as Int
                new CompStmt(
                        new AssignStmt("x", new ValueExp(new BoolValue(true))), // Assign boolean to x
                        new PrintStmt(new VarExp("x"))                          // Attempt to print x
                )
        );
    }
}
*/