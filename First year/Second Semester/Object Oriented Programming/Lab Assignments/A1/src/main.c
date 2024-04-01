#include <stdio.h>
#include <stdbool.h>

void ReadVector(int vector[], int *size);
void PrintMenu();

bool IsPrime(int number);

void ZeroDigitsOfProduct(int vector[], int size);
void LongestContiguousSubsequenceWithAnyTwoConsecutiveElementsBeingPrimeNumbers(const int vector[], int size);
void ExitProgram();

int main() {
    int vector[101], size;
    int choice;

    do {
        PrintMenu();

        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                ReadVector(vector, &size);
                break;
            case 2:
                ZeroDigitsOfProduct(vector, size);
                break;
            case 3:
                LongestContiguousSubsequenceWithAnyTwoConsecutiveElementsBeingPrimeNumbers(vector, size);
                break;
            case 4:
                ExitProgram();
                break;
            default:
                printf("Invalid choice\n");
        }

    } while (choice != 4);

    return 0;
}

/*
 * Reads a vector of integers terminated by 0
 */
void ReadVector(int vector[], int *size) {
    printf("> Enter the elements of the vector (terminate with 0):\n");
    *size = 0;
    do {
        scanf("%d", &vector[*size]);
        (*size)++;
    } while (vector[*size - 1] != 0);
    (*size)--; // Decrement size to exclude the last element that is 0
}

/*
 * Prints the console menu
 */
void PrintMenu()
{
    printf("------------------Menu------------------\n");
    printf("> 1. Read a vector\n");
    printf("> 2. Determine the number of 0 digits of the product of the read numbers.\n");
    printf("> 3. Find the longest contiguous subsequence such that the sum of any two consecutive elements is a prime number.\n");
    printf("> 4. Exit\n");
}

/*
 * Checks if a number is prime
 */
bool IsPrime(int number) {
    if (number < 2)
        return false;
    if (number == 2)
        return true;
    if (number % 2 == 0)
        return false;
    for (int i = 3; i * i <= number; i += 2)
        if (number % i == 0)
            return false;
    return true;
}

/*
 * Determines the number of 0 digits of the product of the given vector then prints the result
 */
void ZeroDigitsOfProduct(int vector[], int size) {
    int p_2 = 0, p_5 = 0, result;
    for (int i = 0; i < size; ++i)
    {
        while (vector[i] % 2 == 0)
        {
            p_2++;
            vector[i] /= 2;
        }
        while (vector[i] % 5 == 0)
        {
            p_5++;
            vector[i] /= 5;
        }
    }
    if (p_2 < p_5)
        result = p_2;
    else
        result = p_5;

    printf("The number of 0 digits of the product of the read numbers is: %d\n", result);
}

/*
 * Finds the longest contiguous subsequence such that the sum of any two consecutive elements is a prime number then prints the length of the subsequence
 */
void LongestContiguousSubsequenceWithAnyTwoConsecutiveElementsBeingPrimeNumbers(const int vector[], int size) {
    int length = 0;
    for (int i = 0; i < size - 1; ++i) {
        int sum = 0;
        for (int j = i; j < size; ++j) {
            sum += vector[j];
            sum += vector[j + 1];
            if (IsPrime(sum)) {
                length += 1;
            }
        }
    }

    printf("The longest contiguous subsequence such that the sum of any two consecutive elements is a prime number is: %d\n", length);
}

/*
 * Exits the program
 */
void ExitProgram() {
    printf("Exiting...\n");
}
