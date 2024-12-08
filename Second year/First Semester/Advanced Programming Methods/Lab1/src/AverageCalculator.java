import java.util.Scanner;

public class AverageCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter the number of integers: ");
        int count = scanner.nextInt();

        int sum = 0;
        System.out.println("Enter " + count + " integers:");

        for (int i = 0; i < count; i++) {
            sum += scanner.nextInt();
        }

        double average = (double) sum / count;
        System.out.println("The average is: " + average);
    }
}
