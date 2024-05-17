#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>


//Write a C program that creates a child process with which it communicates via pipes.
//The parent process reads a natural number from the keyboard and sends it via pipes to the child process,
//and the child process checks and displays whether this number is even or odd.


int main(int argc, char** argv)
{
	int n, p2a[2];
	while(1)
	{
		scanf("%d", &n);
		pipe(p2a);
		if(fork() == 0)
		{
			close(p2a[0]);
			close(p2a[1]);
			if(n % 2 == 0)
				printf("Number is even\n");
			else
				printf("Number is odd\n");
			exit(0);
		}

		close(p2a[0]);
		write(p2a[1], &n, sizeof(int));
		close(p2a[1]);
		wait(0);
	}
	return 0;
}
