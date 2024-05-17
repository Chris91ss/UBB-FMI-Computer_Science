#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/wait.h>

//A process A generates 2 random numbers and reads from the keyboard an arithmetic symbol or 0 (*/:)
//Process A sends process B through pipes the two numbers and the arithmetic symbol and process B performs
//the operation and writes it to a file. The two processes end their execution only when the symbol 0 is read.

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

    if (pid == 0) { // Process B
        close(fd[1]); // Close unused write end

        // Open the file
        FILE *file = fopen("result.txt", "w");
        if (file == NULL) {
            perror("fopen");
            exit(EXIT_FAILURE);
        }

        // Read the numbers and the operation from the pipe and perform the operation
        int x, y;
        char op;
        while (read(fd[0], &x, sizeof(int)) > 0 && read(fd[0], &y, sizeof(int)) > 0 && read(fd[0], &op, sizeof(char)) > 0) {
            int result;
            if (op == '+') {
                result = x + y;
            } else if (op == '-') {
                result = x - y;
            } else if (op == '*') {
                result = x * y;
            } else if (op == '/') {
                if (y != 0) {
                    result = x / y;
                } else {
                    fprintf(stderr, "Error: Division by zero\n");
                    exit(EXIT_FAILURE);
                }
            } else {
                break;
            }

            // Write the result to the file
            fprintf(file, "%d %c %d = %d\n", x, op, y, result);
        }

        fclose(file);
        close(fd[0]); // Close read end
        exit(EXIT_SUCCESS); // Terminate the child process successfully
    } else { // Process A
        close(fd[0]); // Close unused read end

        // Seed the random number generator
        srand(time(NULL));

        // Generate two random numbers and read an operation from the keyboard
        int x, y;
        char op;
        do {
            x = rand() % 100;
            y = rand() % 100;
            printf("Enter an operation (+, -, *, /) or 0 to quit: ");
            scanf(" %c", &op);

            // Write the numbers and the operation to the pipe
            write(fd[1], &x, sizeof(int));
            write(fd[1], &y, sizeof(int));
            write(fd[1], &op, sizeof(char));
        } while (op != '0');

        close(fd[1]); // Close write end

        // Wait for the child process to finish
        wait(NULL);

        exit(EXIT_SUCCESS); // Terminate the parent process successfully
    }

    return 0;
}
