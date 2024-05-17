#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/wait.h>

//Two processes are made, one of them randomly generates an n and reads a k from the keyboard,
//pipes them to the other process. The second process, if k is even sum the digits of n, otherwise
//it makes the product of the digits of n and writes the obtained result to the file.

int sum_digits(int n) {
    int sum = 0;
    while (n != 0) {
        sum += n % 10;
        n /= 10;
    }
    return sum;
}

int product_digits(int n) {
    int product = 1;
    while (n != 0) {
        product *= n % 10;
        n /= 10;
    }
    return product;
}

int main() {
    int fd[2];
    pid_t pid;

    // Create the pipe
    if (pipe(fd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // Fork the process
    pid = fork();

    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // Second process
        close(fd[1]); // Close unused write end

        // Read n and k from the pipe
        int n, k;
        read(fd[0], &n, sizeof(int));
        read(fd[0], &k, sizeof(int));

        // Compute the result
        int result = (k % 2 == 0) ? sum_digits(n) : product_digits(n);

        // Open the file
        FILE *file = fopen("result2.txt", "w");
        if (file == NULL) {
            perror("fopen");
            exit(EXIT_FAILURE);
        }

        // Write the result to the file
        fprintf(file, "%d\n", result);

        fclose(file);
        close(fd[0]); // Close read end
        exit(EXIT_SUCCESS); // Terminate the process successfully
    } else { // First process
        close(fd[0]); // Close unused read end

        // Generate a random number n
        srand(time(NULL));
        int n = rand() % 100;

        // Read k from the keyboard
        int k;
        printf("Enter a number: ");
        scanf("%d", &k);

        // Write n and k to the pipe
        write(fd[1], &n, sizeof(int));
        write(fd[1], &k, sizeof(int));

        close(fd[1]); // Close write end

        // Wait for the second process to finish
        wait(NULL);

        exit(EXIT_SUCCESS); // Terminate the process successfully
    }

    return 0;
}
