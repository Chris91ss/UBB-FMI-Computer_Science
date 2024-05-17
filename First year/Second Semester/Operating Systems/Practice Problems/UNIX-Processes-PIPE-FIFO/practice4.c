#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

//Write a C program that creates a child process with which it communicates via pipes.
//The parent process reads two integers from a text file and sends them via pipes to the child process,
//and the child process pipes back their sum.

int main() {
    int fd1[2], fd2[2];
    pid_t pid;

    // Create the pipes
    if (pipe(fd1) == -1 || pipe(fd2) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // Fork the process
    pid = fork();

    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // Child process
        close(fd1[1]); // Close unused write end of first pipe

        // Read the two integers from the first pipe
        int x, y;
        read(fd1[0], &x, sizeof(int));
        read(fd1[0], &y, sizeof(int));

        // Compute their sum
        int sum = x + y;

        close(fd1[0]); // Close read end of first pipe
        close(fd2[0]); // Close unused read end of second pipe

        // Write the sum back to the second pipe
        write(fd2[1], &sum, sizeof(int));

        close(fd2[1]); // Close write end of second pipe
    } else { // Parent process
        close(fd1[0]); // Close unused read end of first pipe
        close(fd2[1]); // Close unused write end of second pipe

        // Read two integers from a file
        FILE *file = fopen("numbers.txt", "r");
        if (file == NULL) {
            perror("fopen");
            exit(EXIT_FAILURE);
        }

        int x, y;
        fscanf(file, "%d %d", &x, &y);
        fclose(file);

        // Write the integers to the first pipe
        write(fd1[1], &x, sizeof(int));
        write(fd1[1], &y, sizeof(int));

        close(fd1[1]); // Close write end of first pipe

        // Wait for the child process to finish
        wait(NULL);

        // Read the sum from the second pipe
        int sum;
        read(fd2[0], &sum, sizeof(int));

        printf("The sum is %d\n", sum);

        close(fd2[0]); // Close read end of second pipe
    }

    return 0;
}
