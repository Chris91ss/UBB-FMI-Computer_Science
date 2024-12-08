class Motorcycle {
    static int motorcycleCount = 0;

    String name;

    public Motorcycle(String name) throws IllegalArgumentException {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Motorcycle name cannot be null or empty.");
        }
        this.name = name;
        motorcycleCount++;
    }

    public void makeSound() {
        System.out.println("Vroom");
    }

    public static int getMotorcycleCount() {
        return motorcycleCount;
    }
}

class SportMotorcycle extends Motorcycle {
    public SportMotorcycle(String name) throws IllegalArgumentException {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println("Vroom! Vroom! RATATATATA");
    }
}

public class MainClass {
    public static void main(String[] args) {
        try {
            Motorcycle regularBike = new Motorcycle("RegularBike");
            SportMotorcycle sportBike = new SportMotorcycle("SuperSport");

            Motorcycle invalidBike = new Motorcycle("");

            regularBike.makeSound();
            sportBike.makeSound();

            System.out.println("Total motorcycles created: " + Motorcycle.getMotorcycleCount());

        } catch (IllegalArgumentException e) {
            System.out.println("An error occurred: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("An unexpected error occurred: " + e.getMessage());
        }
    }
}
