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

public class Interpreter {
    public static void main(String[] args) {
        // Example 1: int v; v=2; Print(v)
        IStmt ex1 = new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new AssignStmt("v", new ValueExp(new IntValue(2))),
                        new PrintStmt(new VarExp("v"))
                )
        );

        // Initialize Heap
        MyIHeap heap1 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex1
        PrgState prg1 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap1),
                heap1,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap1), // FileTable
                ex1
        );
        IRepository repo1 = new Repository(prg1, "log1.txt");
        Controller ctr1 = new Controller(repo1);

        // Example 2: int a; int b; a=2+3*5; b=a+1; Print(b)
        IStmt ex2 = new CompStmt(
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

        // Initialize Heap
        MyIHeap heap2 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex2
        PrgState prg2 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap2),
                heap2,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap2), // FileTable
                ex2
        );
        IRepository repo2 = new Repository(prg2, "log2.txt");
        Controller ctr2 = new Controller(repo2);

        // Example 3: bool a; a=false; int v; If a Then v=2 Else v=3; Print(v)
        IStmt ex3 = new CompStmt(
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

        // Initialize Heap
        MyIHeap heap3 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex3
        PrgState prg3 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap3),
                heap3,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap3), // FileTable
                ex3
        );
        IRepository repo3 = new Repository(prg3, "log3.txt");
        Controller ctr3 = new Controller(repo3);

        // Example 4: File operations test
        IStmt ex4 = new CompStmt(
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

        // Initialize Heap
        MyIHeap heap4 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex4
        PrgState prg4 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap4),
                heap4,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap4), // FileTable
                ex4
        );
        IRepository repo4 = new Repository(prg4, "log4.txt");
        Controller ctr4 = new Controller(repo4);

        // Example 5: Using relational expressions
        IStmt ex5 = new CompStmt(
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

        // Initialize Heap
        MyIHeap heap5 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex5
        PrgState prg5 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap5),
                heap5,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap5), // FileTable
                ex5
        );
        IRepository repo5 = new Repository(prg5, "log5.txt");
        Controller ctr5 = new Controller(repo5);

        // Example 6: int v; v=4; while (v>0) { print(v); v=v-1; } print(v);
        IStmt ex6 = new CompStmt(
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
        // Initialize Heap
        MyIHeap heap6 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex6
        PrgState prg6 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap6),
                heap6,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap6), // FileTable
                ex6
        );
        IRepository repo6 = new Repository(prg6, "log6.txt");
        Controller ctr6 = new Controller(repo6);




        // Example 7: Testing the Heap
        IStmt ex7 = new CompStmt(
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
        // Initialize Heap
        MyIHeap heap7 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex7
        PrgState prg7 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap7),
                heap7,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap7), // FileTable
                ex7
        );
        IRepository repo7 = new Repository(prg7, "log7.txt");
        Controller ctr7 = new Controller(repo7);


        // Example 8: Testing the Garbage Collector
        IStmt ex8 = new CompStmt(
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

        // Initialize Heap for ex8
        MyIHeap heap8 = new MyHeap();

        // Initialize Symbol Tables and File Tables with the heap
        MyIDictionary<String, Value> symTable8 = new MyDictionary<>(heap8);
        MyIDictionary<StringValue, BufferedReader> fileTable8 = new MyDictionary<>(heap8);

        // Initialize Execution Stack and Output
        MyIStack<IStmt> exeStack8 = new MyStack<>();
        MyIList<Value> out8 = new MyList<>();

        // Create the initial Program State with the selected program
        PrgState prg8 = new PrgState(
                exeStack8,
                symTable8,
                heap8,
                out8,
                fileTable8,
                ex8
        );

        // Create the repository and controller for ex8
        IRepository repo8 = new Repository(prg8, "log8.txt");
        Controller ctr8 = new Controller(repo8);


        // Example 9:
        // int v; Ref int a; v=10; new(a,22);
        // fork(wH(a,30); v=32; print(v); print(rH(a)));
        // print(v); print(rH(a))

        IStmt ex9 = new CompStmt(
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

        // Initialize Heap
        MyIHeap heap9 = new MyHeap();

        // Initialize Program State, Repository, and Controller for ex9
        PrgState prg9 = new PrgState(
                new MyStack<IStmt>(),
                new MyDictionary<String, Value>(heap9),
                heap9,
                new MyList<Value>(),
                new MyDictionary<StringValue, BufferedReader>(heap9),
                ex9
        );

        IRepository repo9 = new Repository(prg9, "log9.txt");
        Controller ctr9 = new Controller(repo9);


        // Create the Text Menu and add commands
        TextMenu menu = new TextMenu();
        menu.addCommand(new ExitCommand("0", "exit"));
        menu.addCommand(new RunExample("1", ex1.toString(), ctr1));
        menu.addCommand(new RunExample("2", ex2.toString(), ctr2));
        menu.addCommand(new RunExample("3", ex3.toString(), ctr3));
        menu.addCommand(new RunExample("4", ex4.toString(), ctr4));
        menu.addCommand(new RunExample("5", ex5.toString(), ctr5));
        menu.addCommand(new RunExample("6", ex6.toString(), ctr6));
        menu.addCommand(new RunExample("7", ex7.toString(), ctr7));
        menu.addCommand(new RunExample("8", ex8.toString(), ctr8));
        menu.addCommand(new RunExample("9", ex9.toString(), ctr9));

        // Display the menu and wait for user input
        menu.show();
    }
}
