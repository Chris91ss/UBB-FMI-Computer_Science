#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#define MAX_STRING_SIZE 256

//Write a C program that creates a child process with which it communicates via pipes.
//The parent process reads a character c and a string s from the keyboard and sends them via pipe to the child process,
//and the child process checks and displays the number of occurrences of the character c in the string s.

int main() {
    int fd[2];
    pid_t pid;
    char c;
    char s[MAX_STRING_SIZE];

    // Create pipe
    if (pipe(fd) == -1) {
        fprintf(stderr, "Pipe failed");
        return 1;
    }

    // Fork a child process
    pid = fork();

    if (pid < 0) { // Error occurred
        fprintf(stderr, "Fork failed");
        return 1;
    } else if (pid > 0) { // Parent process
       	close(fd[0]);
	printf("Enter a character: ");
        scanf(" %c", &c); // Note the space before %c to skip any whitespace characters

        printf("Enter a string: ");
        scanf("%s", s);

        // Write the character and string to the pipe
        write(fd[1], &c, sizeof(char));
        write(fd[1], s, strlen(s) + 1);

        // Close the write end of the pipe
        close(fd[1]);
    } else { // Child process
        char ch;
        char str[MAX_STRING_SIZE];
        int count = 0;
	close(fd[1]);
        // Read the character and string from the pipe
        read(fd[0], &ch, sizeof(char));
        read(fd[0], str, MAX_STRING_SIZE);

        // Count the occurrences of the character in the string
        for (int i = 0; str[i] != '\0'; i++) {
            if (str[i] == ch) {
                count++;
            }
        }

        printf("The character '%c' appears %d times in the string \"%s\".\n", ch, count, str);

        // Close the read end of the pipe
        close(fd[0]);
    }
    wait(0);
    return 0;
}
