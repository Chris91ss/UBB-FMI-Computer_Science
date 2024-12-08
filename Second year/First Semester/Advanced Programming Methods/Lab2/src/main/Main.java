package main;

import controller.VehicleController;
import model.Car;
import model.Motorcycle;
import model.Truck;
import model.Vehicle;
import repository.VehicleRepository;
import view.VehicleView;

public class Main {
    public static void main(String[] args) {
        VehicleRepository repository = new VehicleRepository(10);
        VehicleController controller = new VehicleController(repository);
        VehicleView view = new VehicleView(controller);
        view.start();
    }
}
