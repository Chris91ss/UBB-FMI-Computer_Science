#include <stdlib.h>
#include <stdio.h>
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
    int p2a[2], a2p[2], a2b[2];
    pipe(p2a);
    pipe(a2p);
    pipe(a2b);

    if (fork() == 0) {
        // Child Process B
        close(p2a[0]);
        close(p2a[1]);
        close(a2p[0]);
        close(a2p[1]);
        close(a2b[1]);

        int v[26];
        while (1) {
            if (read(a2b[0], v, 26 * sizeof(int)) <= 0)
                break;

            int sum = 0;
            for (int i = 0; i < 26; i++)
                sum += v[i];
            printf("The sum of all letters: %d\n", sum);
        }
        close(a2b[0]);
        exit(0);
    }

    if (fork() == 0) {
        // Child Process A
        close(p2a[1]);
        close(a2p[0]);
        close(a2b[0]);

        char s[100];
        while (1) {
            int n;
            if (read(p2a[0], &n, sizeof(int)) <= 0)
                break;
            if (n == 0) // End of input
                break;

            if (read(p2a[0], s, n * sizeof(char)) <= 0)
                break;

            int v[26] = {0};
            for (int i = 0; i < n; i++) {
                if (s[i] >= 'a' && s[i] <= 'z') {
                    int idx = s[i] - 'a';
                    v[idx]++;
                }
            }

            write(a2b[1], v, 26 * sizeof(int));
            write(a2p[1], v, 26 * sizeof(int));
        }

        close(p2a[0]);
        close(a2b[1]);
        close(a2p[1]);
        exit(0);
    }

    // Parent Process
    close(a2b[0]);
    close(a2p[1]);
    close(p2a[0]);

    char s[100];
    int n;
    int v[26];

    do {
        printf("Insert a string containing lowercase letters: ");
        fgets(s,sizeof(s),stdin);
        if (s[0] == 'x')
        {  
            printf("Exiting");
            break;
        }

        n = strlen(s);
        write(p2a[1], &n, sizeof(int));
        write(p2a[1], s, n * sizeof(char));

        if (read(a2p[0], v, 26 * sizeof(int)) < 0)
            break;
        
        for (int i = 0; i < 26; i++) {
            char c = 'a' + i;
            printf("%c -> %d\n", c, v[i]);
        }
    } while (1);

    close(p2a[1]);
    close(a2p[0]);

    wait(0); // Wait for child processes to finish
    wait(0);

    return 0;
}