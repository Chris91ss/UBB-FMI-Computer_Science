package repository;
import model.Vehicle;

public interface Repository {
    void addVehicle(Vehicle vehicle);
    void removeVehicle(int index);
    Vehicle[] getAllVehicles();
}
