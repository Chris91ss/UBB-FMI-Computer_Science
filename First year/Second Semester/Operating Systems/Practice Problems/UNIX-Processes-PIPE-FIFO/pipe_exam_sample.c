#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
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
//    Will receive the frequency vector from the a child process A with a pipe and it will sum up all the values and print the sum



int main(int argc, char** argv)
{
	int p2a[2], a2p[2], a2b[2];

	while(1)
	{
		char s[101];
		int v[27] = {0};
		pipe(p2a);
		pipe(a2p);
		pipe(a2b);

		printf("Enter a string or x to stop: ");
		scanf("%s", s);
		if(s[0] == 'x')
			break;

		// Process A
		if(fork() == 0)
		{
			close(p2a[1]); close(a2p[0]); close(a2b[0]);
			read(p2a[0], s, sizeof(s));
			close(p2a[0]);
			for(int i = 0; i < 26; i++)
				v[i] = 0;

			for(int i = 0; i < strlen(s); i++)
			{
				int poz = s[i] - 'a';
				v[poz]++;
			}				
			write(a2p[1], v, sizeof(v));
			close(a2p[1]);
			write(a2b[1], v, sizeof(v));
			close(a2b[1]);
			exit(1);		
		}
		
		// Process B
		if(fork() == 0)
		{
			close(p2a[0]); close(p2a[1]);
			close(a2p[0]); close(a2p[1]);
			close(a2b[1]);
			read(a2b[0], v, sizeof(v));
			close(a2b[0]);

			int sum = 0;
			for(int i = 0; i < 26; i++)
				sum += v[i];

			printf("The sum is: %d\n", sum);

			exit(1);
		}

		// Parent process
		close(a2b[0]), close(a2b[1]);
		close(p2a[0]);
		write(p2a[1], s, sizeof(s));
		close(p2a[1]);
		close(a2p[1]);	
		read(a2p[0], v, sizeof(v));
		close(a2p[0]);	
		for(int i = 0; i < 26; i++)
		{
			printf("%d ", v[i]);
		}
		printf("\n");
	}

	wait(0);
	wait(0);

	return 0;
}
