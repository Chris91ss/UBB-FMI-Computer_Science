package view;

import controller.Controller;
import exceptions.InterpreterException;
import model.state.PrgState;

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
            ctr.allStep();

            // After execution, get the final program state and display the output
            PrgState prgState = ctr.getRepo().getCrtPrg();
            System.out.println("Final Program State:");
            System.out.println(prgState.toString());
            System.out.println("Output:");
            System.out.println(prgState.getOut().toString());
        } catch (InterpreterException e) {
            System.out.println("Error: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Unexpected error: " + e.getMessage());
        }
    }
}