package model;

public class Car implements Vehicle {
    private final int repairCost;

    public Car(int repairCost) {
        this.repairCost = repairCost;
    }

    public int getRepairCost() {
        return repairCost;
    }
}
