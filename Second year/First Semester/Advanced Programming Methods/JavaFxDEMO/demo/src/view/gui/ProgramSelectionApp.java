package view.gui;

import exceptions.DictionaryException;
import exceptions.ExpressionException;
import exceptions.StatementException;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import model.datastructures.*;
import model.exp.*;
import model.stmt.*;
import model.types.*;
import model.values.*;
import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.List;

/**
 * A JavaFX app listing example programs.  Selecting one opens MainWindow.
 */
public class ProgramSelectionApp extends Application {

    private final List<IStmt> programs = new ArrayList<>();

    @Override
    public void start(Stage primaryStage) {
        initializePrograms();

        ListView<String> programList = new ListView<>();
        for (IStmt stmt : programs) {
            programList.getItems().add(stmt.toString());
        }

        Button selectBtn = new Button("Select Program");
        selectBtn.setOnAction(e -> {
            int idx = programList.getSelectionModel().getSelectedIndex();
            if (idx < 0) return;

            IStmt chosen = programs.get(idx);
            // Open the MainWindow
            MainWindow mainWin = new MainWindow(chosen);
            mainWin.show();

            // close this selection window
            primaryStage.close();
        });

        VBox root = new VBox(10, programList, selectBtn);
        Scene scene = new Scene(root, 600, 400);
        primaryStage.setTitle("Select a ToyLanguage Program");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void initializePrograms() {
        IStmt ex1  = example1();
        IStmt ex2  = example2();
        IStmt ex3  = example3();
        IStmt ex4  = example4();
        IStmt ex5  = example5();
        IStmt ex6  = example6();
        IStmt ex7  = example7();
        IStmt ex8  = example8();
        IStmt ex9  = example9();
        IStmt ex10 = example10(); // Type error example

        doTypeCheckAndAdd(ex1);
        doTypeCheckAndAdd(ex2);
        doTypeCheckAndAdd(ex3);
        doTypeCheckAndAdd(ex4);
        doTypeCheckAndAdd(ex5);
        doTypeCheckAndAdd(ex6);
        doTypeCheckAndAdd(ex7);
        doTypeCheckAndAdd(ex8);
        doTypeCheckAndAdd(ex9);
        doTypeCheckAndAdd(ex10);
    }

    private void doTypeCheckAndAdd(IStmt stmt) {
        MyIHeap typeHeap = new MyHeap();
        MyIDictionary<String, Type> typeEnv = new MyDictionary<>(typeHeap);
        try {
            stmt.typecheck(typeEnv);
            programs.add(stmt);
        } catch (StatementException | ExpressionException | DictionaryException ex) {
            System.out.println("TypeCheck failed: " + ex.getMessage());
        }
    }

    // Example 1: int v; v=2; Print(v)
    private IStmt example1() {
        return new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new AssignStmt("v", new ValueExp(new IntValue(2))),
                        new PrintStmt(new VarExp("v"))
                )
        );
    }

    // Example 2: int a; int b; a=2+3*5; b=a+1; Print(b)
    private IStmt example2() {
        return new CompStmt(
                new VarDeclStmt("a", new IntType()),
                new CompStmt(
                        new VarDeclStmt("b", new IntType()),
                        new CompStmt(
                                new AssignStmt("a",
                                        new ArithExp(1,
                                                new ValueExp(new IntValue(2)),
                                                new ArithExp(3,
                                                        new ValueExp(new IntValue(3)),
                                                        new ValueExp(new IntValue(5)))
                                        )
                                ),
                                new CompStmt(
                                        new AssignStmt("b",
                                                new ArithExp(1,
                                                        new VarExp("a"),
                                                        new ValueExp(new IntValue(1)))
                                        ),
                                        new PrintStmt(new VarExp("b"))
                                )
                        )
                )
        );
    }

    // Example 3: bool a; a=false; int v; if a then v=2 else v=3; print(v)
    private IStmt example3() {
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

    // Example 4: File operations
    private IStmt example4() {
        /*
         string varf; varf="test.in";
         openRFile(varf);
         int varc;
         readFile(varf,varc); print(varc);
         readFile(varf,varc); print(varc);
         closeRFile(varf);
         */
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

    // Example 5: Using relational expressions
    private IStmt example5() {
        /*
         int a,b; a=10; b=20;
         if (a<b) print("a<b") else print("a>=b");
         if (a-5 > b) ...
         if (a==b) ...
         print("End");
         */
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
                                                                new RelationalExp(">", new ArithExp(2,
                                                                        new VarExp("a"),
                                                                        new ValueExp(new IntValue(5))
                                                                ), new VarExp("b")),
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

    // Example 6: int v; v=4; while(v>0) {print(v); v=v-1;} print(v);
    private IStmt example6() {
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

    // Example 7: Testing the Heap
    private IStmt example7() {
        /*
         int v; Ref int a; v=10; new(a, v);
         print(rH(a));
         wH(a, 20);
         print(rH(a));
         */
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

    // Example 8: Testing the Garbage Collector
    private IStmt example8() {
        /*
         Ref int a; Ref int b; new(a,10); new(b,20);
         print(rH(a)); print(rH(b));
         a=b;
         print(rH(a)); print(rH(b));
         */
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
                                                                new AssignStmt("a", new VarExp("b")),
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

    // Example 9: concurrency & heap
    private IStmt example9() {
        /*
         int v; Ref int a; v=10; new(a,22);
         fork(wH(a,30); v=32; print(v); print(rH(a)));
         print(v); print(rH(a));
         */
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

    // Example 10: Type Error example
    private IStmt example10() {
        // int x; x=true; print(x);
        return new CompStmt(
                new VarDeclStmt("x", new IntType()),
                new CompStmt(
                        new AssignStmt("x", new ValueExp(new BoolValue(true))),
                        new PrintStmt(new VarExp("x"))
                )
        );
    }

    public static void main(String[] args) {
        launch(args);
    }
}
