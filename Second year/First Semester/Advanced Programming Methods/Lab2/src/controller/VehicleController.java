package controller;

import model.Vehicle;
import repository.VehicleRepository;

import java.util.Arrays;

public class VehicleController {
    private VehicleRepository repository;

    public VehicleController(VehicleRepository repository) {
        this.repository = repository;
    }

    public void addVehicle(Vehicle vehicle) {
        repository.addVehicle(vehicle);
    }

    public void removeVehicle(int index) {
        repository.removeVehicle(index);
    }

    public Vehicle[] getVehiclesWithRepairCostOver1000()
    {
        Vehicle[] vehicles = repository.getAllVehicles();
        return Arrays.stream(vehicles)
                .filter(vehicle -> vehicle.getRepairCost() > 1000)
                .toArray(Vehicle[]::new);
    }

    public Vehicle[] getAllVehicles()
    {
        return repository.getAllVehicles();
    }
}
