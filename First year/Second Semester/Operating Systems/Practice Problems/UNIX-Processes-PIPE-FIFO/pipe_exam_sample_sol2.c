#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>

//Write a C program that will read from keyboard lowercased strings (until X is written).
//The main process will start two types of Child processes: A and B started every time a string is read from the keyboard

//Child processes A.
//    The parent will send the string to the created child process using pipes.

//    Each child process will initiate a vector V with 26 zeros and will iterate over the string character by character trying to compute an index considering the ASCII code of a character:
//    a (97) -> 0
//    b (98) -> 1
//    c (99) -> 2
//    etc.

//    This index corresponds to a position in vector V that will have to be incremented during each character iteration.
//    This frequency vector for the characters found in the string will be send back:
//        - to the parent using pipes that will print it on the screen.
//        - to the process B

//Child processes B:
//    Will receive the frequency vector from the a child process A with a pipe and it will sum up all the values and print the


int main(int argc, char **argv)
{
    int a2p[2], p2a[2];
    pipe(a2p);
    pipe(p2a);
    int b2p[2], p2b[2];
    pipe(b2p);
    pipe(p2b);

    if (fork() == 0) {
        // Child Process B
        close(a2p[1]);
        close(p2a[0]);
        close(b2p[0]);
        close(p2b[1]);

        char s[100];
        int n, sum;

        while (1) {
            if (read(p2b[0], &n, sizeof(int)) <= 0)
                break;
            read(p2b[0], s, n * sizeof(char));
            s[n] = '\0';

            sum = 0;
            char *token = strtok(s, " ");
            while (token != NULL) {
                sum += atoi(token);
                token = strtok(NULL, " ");
            }

            write(b2p[1], &sum, sizeof(int));
        }

        close(b2p[1]);
        close(p2b[0]);
        exit(0);
    }

    if (fork() == 0) {
        // Child Process A
        close(b2p[0]);
        close(b2p[1]);
        close(p2b[0]);
        close(p2b[1]);
        close(a2p[0]);
        close(a2p[1]);
        close(p2a[0]);
        close(p2a[1]);

        char s[100];
        int n, v[10] = {0};

        while (1) {
            if (read(p2a[0], &n, sizeof(int)) <= 0)
                break;
            read(p2a[0], s, n * sizeof(char));
            s[n] = '\0';

            char *token = strtok(s, " ");
            while (token != NULL) {
                int num = atoi(token);
                if (num >= 0 && num <= 9)
                    v[num]++;
                token = strtok(NULL, " ");
            }
        }

        exit(0);
    }

    // Parent Process
    close(a2p[0]);
    close(a2p[1]);
    close(p2a[0]);
    close(p2a[1]);
    close(b2p[0]);
    close(b2p[1]);
    close(p2b[0]);
    close(p2b[1]);

    char s[100];
    int n, v[10];

    do {
        printf("Insert a string of numbers separated by space: ");
        fgets(s, sizeof(s), stdin);
        if (s[0] == 'x')
            break;

        n = strlen(s);
        write(p2a[1], &n, sizeof(int));
        write(p2a[1], s, n * sizeof(char));

        // Read frequency vector from child process A
        read(a2p[0], v, 10 * sizeof(int));
        for (int i = 0; i < 10; i++) {
            printf("The character %d appears %d times in the string\n", i, v[i]);
        }

        // Write input
        write(p2b[1], &n, sizeof(int));
        write(p2b[1], s, n * sizeof(char));

        // Read sum from child process B
        read(b2p[0], &n, sizeof(int));
        printf("The sum of the numbers is: %d\n", n);

    } while (s[0] != 'x');

    close(a2p[0]);
    close(p2a[1]);
    close(b2p[0]);
    close(p2b[1]);

    // Wait for child processes to finish
    wait(0);
    wait(0);

    return 0;
}
