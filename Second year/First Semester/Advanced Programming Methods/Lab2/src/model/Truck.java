package model;

public class Truck implements Vehicle {
    private final int repairCost;

    public Truck(int repairCost) {
        this.repairCost = repairCost;
    }

    public int getRepairCost() {
        return repairCost;
    }
}
