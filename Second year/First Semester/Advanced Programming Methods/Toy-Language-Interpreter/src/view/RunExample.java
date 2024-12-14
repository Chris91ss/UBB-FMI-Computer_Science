package view;

import controller.Controller;
import exceptions.InterpreterException;
import model.datastructures.MyIList;
import model.state.PrgState;
import model.values.Value;

import java.util.List;
import java.util.Scanner;

public class RunExample extends Command {
    private Controller ctr;

    public RunExample(String key, String desc, Controller ctr) {
        super(key, desc);
        this.ctr = ctr;
    }

    @Override
    public void execute() {
        try {
            Scanner scanner = new Scanner(System.in);
            System.out.print("Display program state after each execution step? (yes/no): ");
            String displayOption = scanner.nextLine();
            boolean displayFlag = displayOption.equalsIgnoreCase("yes") || displayOption.equalsIgnoreCase("y");
            ctr.setDisplayFlag(displayFlag);

            // Store a reference to 'Out' from the initial PrgState before execution
            List<PrgState> initialStates = ctr.getRepo().getPrgList();
            MyIList<Value> outReference = null;
            if (!initialStates.isEmpty()) {
                outReference = initialStates.get(0).getOut();
            }

            ctr.allStep();

            // After execution, get the final list of program states
            List<PrgState> finalStates = ctr.getRepo().getPrgList();

            if (finalStates.isEmpty()) {
                System.out.println("No program states left after execution.");
                // Print output from outReference if available
                if (outReference != null) {
                    System.out.println("Output:");
                    System.out.println(outReference.toString());
                }
            } else {
                System.out.println("Final Program States:");
                for (PrgState prgState : finalStates) {
                    System.out.println(prgState.toString());
                }

                // Output is shared, print from the first state
                System.out.println("Output:");
                System.out.println(finalStates.get(0).getOut().toString());
            }
        } catch (InterpreterException e) {
            System.out.println("Error: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Unexpected error: " + e.getMessage());
        }
    }


}
