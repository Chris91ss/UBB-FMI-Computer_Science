package model;

public class Motorcycle implements Vehicle {
    private final int repairCost;

    public Motorcycle(int repairCost) {
        this.repairCost = repairCost;
    }

    public int getRepairCost()
    {
        return repairCost;
    }
}
