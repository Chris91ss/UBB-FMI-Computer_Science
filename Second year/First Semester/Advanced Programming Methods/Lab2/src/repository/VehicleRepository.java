package repository;

import model.Vehicle;

public class VehicleRepository implements Repository {
    private Vehicle[] vehicles;
    private int currentIndex = 0;

    public VehicleRepository(int size) {
        vehicles = new Vehicle[size];
    }

    @Override
    public void addVehicle(Vehicle vehicle) {
        if(currentIndex >= vehicles.length) {
            throw new RuntimeException("Repository is full");
        }
        vehicles[currentIndex++] = vehicle;
    }

    @Override
    public void removeVehicle(int index) {
        if(index < 0 || index >= currentIndex) {
            throw new RuntimeException("Invalid index");
        }
        for(int i = index; i < currentIndex - 1; i++) {
            vehicles[i] = vehicles[i + 1];
        }
        vehicles[--currentIndex] = null;
    }

    @Override
    public Vehicle[] getAllVehicles() {
        Vehicle[] result = new Vehicle[currentIndex];
        System.arraycopy(vehicles, 0, result, 0, currentIndex);
        return result;
    }
}
