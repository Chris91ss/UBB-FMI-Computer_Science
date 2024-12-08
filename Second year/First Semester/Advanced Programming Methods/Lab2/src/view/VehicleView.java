package view;

import controller.VehicleController;
import model.Vehicle;

import java.util.Scanner;

public class VehicleView {
    private final VehicleController controller;
    private final Scanner scanner;

    public VehicleView(VehicleController controller) {
        this.controller = controller;
        this.scanner = new Scanner(System.in);
    }

    public void start()
    {
        boolean running = true;
        while(running)
        {
            System.out.println("\n=== Vehicle Service System ===");
            System.out.println("1. Add a Vehicle");
            System.out.println("2. Delete a Vehicle");
            System.out.println("3. Display Vehicles with Repair Cost Over 1000 RON");
            System.out.println("4. Display All Vehicles");
            System.out.println("0. Exit");
            System.out.println("Choose an option: ");

            int choice = scanner.nextInt();
            switch (choice) {
                case 1:
                    addVehicle();
                    break;
                case 2:
                    deleteVehicle();
                    break;
                case 3:
                    displayExpensiveVehicles();
                    break;
                case 4:
                    displayAllVehicles();
                    break;
                case 0:
                    running = false;
                    System.out.println("Exiting...");
                    break;
                default:
                    System.out.println("Invalid Choice! Try Again.");
            }
        }
    }

    private void addVehicle()
    {
        System.out.println("\nSelect Vehicle Type:");
        System.out.println("1. Car");
        System.out.println("2. Truck");
        System.out.println("3. Motorcycle");
        System.out.print("Enter your choice: ");
        int vehicleType = scanner.nextInt();

        System.out.print("Enter repair cost: ");
        int cost = scanner.nextInt();

        switch (vehicleType) {
            case 1:
                controller.addVehicle(new model.Car(cost));
                System.out.println("Car added.");
                break;
            case 2:
                controller.addVehicle(new model.Truck(cost));
                System.out.println("Truck added.");
                break;
            case 3:
                controller.addVehicle(new model.Motorcycle(cost));
                System.out.println("Motorcycle added.");
                break;
            default:
                System.out.println("Invalid vehicle type.");
        }
    }

    private void deleteVehicle()
    {
        System.out.print("Enter the index of the vehicle to delete (0-based index): ");
        int index = scanner.nextInt();
        try {
            controller.removeVehicle(index);
            System.out.println("Vehicle removed.");
        } catch (RuntimeException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private void displayExpensiveVehicles()
    {
        Vehicle[] expensiveVehicles = controller.getVehiclesWithRepairCostOver1000();
        if (expensiveVehicles.length == 0) {
            System.out.println("No vehicles with repair cost over 1000 RON.");
        } else {
            System.out.println("Vehicles with repair cost over 1000 RON:");
            for (Vehicle v : expensiveVehicles) {
                System.out.println(v.getClass().getSimpleName() + " with repair cost: " + v.getRepairCost());
            }
        }
    }

    private void displayAllVehicles()
    {
        Vehicle[] vehicles = controller.getAllVehicles();
        if (vehicles.length == 0) {
            System.out.println("No vehicles.");
        } else {
            System.out.println("All vehicles:");
            for (Vehicle v : vehicles) {
                System.out.println(v.getClass().getSimpleName() + " with repair cost: " + v.getRepairCost());
            }
        }
    }
}
