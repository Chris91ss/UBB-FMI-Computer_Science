#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

//Write a C program that creates a child process with which it communicates via pipes.
//The parent process reads two integers from the keyboard and sends them via pipes to the child process,
//and the child process pipes back their sum.

int main(int argc, char** argv)
{
    int a, b;
    printf("Enter two numbers:");
    scanf("%d %d", &a, &b);
    
    int p[2], p2[2];
    pipe(p);
    pipe(p2);
    if(fork() == 0)
    {
        close(p[1]); // Close writing end of the pipe in the child process
	close(p2[0]); 
        int n1, n2; 
        int sum = 0;
        read(p[0], &n1, sizeof(int));
        read(p[0], &n2, sizeof(int));
        close(p[0]); // Close reading end of the pipe in the child process
        
        sum = n1 + n2;
        
	write(p2[1], &sum, sizeof(int));
	close(p2[1]);
        exit(0);
    }
    close(p[0]); // Close reading end of the pipe in the parent process
    close(p2[1]);
    write(p[1], &a, sizeof(int));
    write(p[1], &b, sizeof(int));
    close(p[1]); // Close writing end of the pipe in the parent process

    int sum = 0; 
    read(p2[0], &sum, sizeof(int));
    close(p2[0]);
    printf("The sum is: %d \n", sum);
    wait(NULL); // Wait for the child process to finish

    return 0;
}
