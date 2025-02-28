package view.gui;

import controller.Controller;
import exceptions.InterpreterException;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;
import model.datastructures.MyDictionary;
import model.datastructures.MyHeap;
import model.datastructures.MyIHeap;
import model.datastructures.MyIStack;
import model.datastructures.MyList;
import model.datastructures.MyIDictionary;
import model.state.PrgState;
import model.stmt.IStmt;
import model.values.StringValue;
import model.values.Value;
import repository.IRepository;
import repository.Repository;

import java.io.BufferedReader;
import java.util.*;
import java.util.stream.Collectors;

/**
 * A JavaFX window that shows the interpreter data and two run buttons.
 * Also a "Back" button to re-select a program from ProgramSelectionApp.
 */
public class MainWindow {
    private Stage stage;
    private Controller controller;

    // UI
    private TextField prgStateCountField;
    private TableView<HeapEntry> heapTableView;
    private ListView<String> outListView;
    private ListView<String> fileTableListView;
    private ListView<Integer> prgStateIdListView;
    private TableView<SymEntry> symTableView;
    private ListView<String> exeStackListView;
    private Button runOneStepButton;
    private Button runAllStepsButton;
    private Button backButton; // new

    // Data for TableViews
    public static class HeapEntry {
        private final Integer address;
        private final String value;
        public HeapEntry(Integer address, String value) {
            this.address = address;
            this.value = value;
        }
        public Integer getAddress() { return address; }
        public String getValue() { return value; }
    }
    public static class SymEntry {
        private final String varName;
        private final String value;
        public SymEntry(String varName, String value) {
            this.varName = varName;
            this.value = value;
        }
        public String getVarName() { return varName; }
        public String getValue() { return value; }
    }

    public MainWindow(IStmt selectedProgram) {
        // Build the ADTs
        MyIStack<IStmt> stack = new model.datastructures.MyStack<>();
        stack.push(selectedProgram);

        MyIHeap heap = new MyHeap();
        MyDictionary<String, Value> symTable = new MyDictionary<>(heap);
        MyList<Value> out = new MyList<>();
        MyDictionary<StringValue, BufferedReader> fileTable = new MyDictionary<>(heap);

        // Build the program state
        PrgState prg = new PrgState(stack, symTable, heap, out, fileTable, selectedProgram);

        // Create Repo & Controller
        IRepository repo = new Repository(prg, "log.txt");
        this.controller = new Controller(repo);

        initializeUI();
    }

    private void initializeUI() {
        stage = new Stage();
        stage.setTitle("ToyLanguage Interpreter - MainWindow");

        prgStateCountField = new TextField();
        prgStateCountField.setEditable(false);

        runOneStepButton = new Button("Run one step");
        runOneStepButton.setOnAction(e -> onRunOneStep());

        runAllStepsButton = new Button("Run entire program");
        runAllStepsButton.setOnAction(e -> onRunAllSteps());

        // "Back" to ProgramSelectionApp
        backButton = new Button("Back to selection");
        backButton.setOnAction(e -> {
            stage.close();
            ProgramSelectionApp newSel = new ProgramSelectionApp();
            newSel.start(new Stage());
        });

        HBox bottomBox = new HBox(10, runOneStepButton, runAllStepsButton, backButton);

        // Setup the Heap Table
        heapTableView = new TableView<>();
        TableColumn<HeapEntry, Integer> addressCol = new TableColumn<>("Address");
        addressCol.setCellValueFactory(data ->
                new javafx.beans.property.SimpleObjectProperty<>(data.getValue().getAddress()));
        TableColumn<HeapEntry, String> valueCol = new TableColumn<>("Value");
        valueCol.setCellValueFactory(data ->
                new javafx.beans.property.SimpleStringProperty(data.getValue().getValue()));
        heapTableView.getColumns().addAll(addressCol, valueCol);

        outListView = new ListView<>();
        fileTableListView = new ListView<>();

        prgStateIdListView = new ListView<>();
        prgStateIdListView.getSelectionModel().selectedItemProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal != null) {
                populateSymTableAndExeStack(newVal);
            }
        });

        symTableView = new TableView<>();
        TableColumn<SymEntry, String> varNameCol = new TableColumn<>("Variable");
        varNameCol.setCellValueFactory(data ->
                new javafx.beans.property.SimpleStringProperty(data.getValue().getVarName()));
        TableColumn<SymEntry, String> varValueCol = new TableColumn<>("Value");
        varValueCol.setCellValueFactory(data ->
                new javafx.beans.property.SimpleStringProperty(data.getValue().getValue()));
        symTableView.getColumns().addAll(varNameCol, varValueCol);

        exeStackListView = new ListView<>();

        BorderPane root = new BorderPane();
        root.setTop(prgStateCountField);
        root.setBottom(bottomBox);

        GridPane centerGrid = new GridPane();
        centerGrid.setHgap(10);
        centerGrid.setVgap(10);

        Label heapLabel = new Label("Heap");
        centerGrid.add(heapLabel, 0, 0);
        centerGrid.add(heapTableView, 1, 0);

        Label outLabel = new Label("Out");
        centerGrid.add(outLabel, 0, 1);
        centerGrid.add(outListView, 1, 1);

        Label fileTblLabel = new Label("FileTable");
        centerGrid.add(fileTblLabel, 0, 2);
        centerGrid.add(fileTableListView, 1, 2);

        Label prgIDLabel = new Label("PrgState IDs");
        centerGrid.add(prgIDLabel, 0, 3);
        centerGrid.add(prgStateIdListView, 1, 3);

        Label symTableLabel = new Label("SymTable");
        centerGrid.add(symTableLabel, 0, 4);
        centerGrid.add(symTableView, 1, 4);

        Label exeStackLabel = new Label("ExeStack");
        centerGrid.add(exeStackLabel, 0, 5);
        centerGrid.add(exeStackListView, 1, 5);

        root.setCenter(centerGrid);

        Scene scene = new Scene(root, 900, 600);
        stage.setScene(scene);
    }

    private void onRunOneStep() {
        try {
            // If no states left, skip
            if (controller.getRepo().getPrgList().isEmpty()) {
                showError("Program has already finished. No states left.");
                return;
            }

            controller.oneStepGUI();
            refreshAll();
        } catch (InterpreterException ex) {
            showError(ex.getMessage());
        } catch (RuntimeException re) {
            showError(re.getMessage());
        }
    }

    private void onRunAllSteps() {
        try {
            if (controller.getRepo().getPrgList().isEmpty()) {
                showError("Program has already finished. No states left.");
                return;
            }
            controller.allStep();
            refreshAll(); // This must happen AFTER allStep()
        } catch (InterpreterException | RuntimeException ex) {
            showError(ex.getMessage());
        }
    }


    private void showError(String msg) {
        Alert alert = new Alert(Alert.AlertType.ERROR, "Execution error: " + msg);
        alert.showAndWait();
    }

    /**
     * Re-populate the UI from the states in the repository.
     */
    private void refreshAll() {
        List<PrgState> prgList = controller.getRepo().getPrgList();

        // 1) Program count
        prgStateCountField.setText("Number of PrgStates: " + prgList.size());

        // 2) IDs
        List<Integer> ids = prgList.stream()
                .map(PrgState::getId)
                .collect(Collectors.toList());
        prgStateIdListView.getItems().setAll(ids);

        // if any selection is chosen, update sym/stack
        Integer chosenId = prgStateIdListView.getSelectionModel().getSelectedItem();
        if (chosenId != null) {
            populateSymTableAndExeStack(chosenId);
        }

        // 3) Heap
        populateHeapTable();

        // 4) Out
        populateOutList();

        // 5) FileTable
        populateFileTable();
    }

    private void populateHeapTable() {
        List<HeapEntry> heapEntries = new ArrayList<>();
        List<PrgState> prgList = controller.getRepo().getPrgList();
        if (!prgList.isEmpty()) {
            PrgState prg = prgList.get(0); // assume single shared heap
            Map<Integer, Value> heapMap = prg.getHeap().getContent();
            for (Map.Entry<Integer, Value> e : heapMap.entrySet()) {
                heapEntries.add(new HeapEntry(e.getKey(), e.getValue().toString()));
            }
        }
        heapTableView.getItems().setAll(heapEntries);
    }

    private void populateOutList() {
        List<PrgState> prgList = controller.getRepo().getPrgList();
        if (!prgList.isEmpty()) {
            PrgState prg = prgList.get(0);
            List<Value> outVals = prg.getOut().getList();
            List<String> outStrings = outVals.stream()
                    .map(Value::toString)
                    .collect(Collectors.toList());
            outListView.getItems().setAll(outStrings);
        } else {
            outListView.getItems().clear();
        }
    }

    private void populateFileTable() {
        List<PrgState> prgList = controller.getRepo().getPrgList();
        if (!prgList.isEmpty()) {
            PrgState prg = prgList.get(0);
            Map<StringValue, BufferedReader> fileMap = prg.getFileTable().getContent();
            List<String> fileNames = fileMap.keySet().stream()
                    .map(StringValue::toString)
                    .collect(Collectors.toList());
            fileTableListView.getItems().setAll(fileNames);
        } else {
            fileTableListView.getItems().clear();
        }
    }

    private void populateSymTableAndExeStack(int prgStateId) {
        PrgState selected = findPrgStateById(prgStateId);
        if (selected == null) return;

        // fill symtable
        List<SymEntry> symData = new ArrayList<>();
        Map<String, Value> symMap = selected.getSymTable().getContent();
        for (Map.Entry<String, Value> e : symMap.entrySet()) {
            symData.add(new SymEntry(e.getKey(), e.getValue().toString()));
        }
        symTableView.getItems().setAll(symData);

        // fill exeStack
        List<String> stackData = new ArrayList<>();
        // top is last in a Java stack
        Stack<IStmt> st = selected.getStk().getStack();
        for (int i = st.size() - 1; i >= 0; i--) {
            stackData.add(st.get(i).toString());
        }
        exeStackListView.getItems().setAll(stackData);
    }

    private PrgState findPrgStateById(int id) {
        for (PrgState p : controller.getRepo().getPrgList()) {
            if (p.getId() == id) {
                return p;
            }
        }
        return null;
    }

    public void show() {
        stage.show();
        refreshAll();
    }
}
